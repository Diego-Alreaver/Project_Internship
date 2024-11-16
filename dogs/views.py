import requests, os
from django.core.cache import cache
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from dotenv import load_dotenv
from .models import DogBreed
from rest_framework.permissions import IsAdminUser
from .serializers import DogBreedSerializer, DogBreedHistorySerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

load_dotenv() 
GIPHY_API_KEY = os.getenv('GIPHY_API_KEY')
DOGS_API_URL = "https://api.thedogapi.com/v1/breeds"

# Define el esquema del parámetro esperado
breed_param = openapi.Parameter(
    'breed',
    openapi.IN_BODY,
    description="Breed name to fetch details and image",
    type=openapi.TYPE_STRING
)

@swagger_auto_schema(
    method='post',
    operation_description="Fetch dog breed details and a gif from Giphy.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'breed': openapi.Schema(type=openapi.TYPE_STRING, description='Dog breed name')
        },
        required=['breed']
    ),
    responses={
        200: "Success - Returns details of the dog breed",
        400: "Bad Request - Breed not specified",
        404: "Not Found - Breed not found in external API"
    }
)

# I chose @api_view instead of APIVIEW (class-based) to keep it simple
@api_view(['POST'])
def fetch_breed_details(request):
    breed_name = request.data.get('breed', '')

    if breed_name:
        # Obtener información de la raza de perro desde la API externa
        dog_api_url = f"https://api.thedogapi.com/v1/breeds/search?q={breed_name}"
        response = requests.get(dog_api_url)

        if response.status_code == 200 and response.json():
            dog_data = response.json()[0]
            dog_breed_name = dog_data.get('name', 'No name available')
            dog_temperament = dog_data.get('temperament', 'No temperament information available')

            # Obtener imagen desde Giphy
            giphy_url = f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_API_KEY}&q={breed_name}&limit=1"
            giphy_response = requests.get(giphy_url)

            dog_image_url = "No image available"
            if giphy_response.status_code == 200 and giphy_response.json()['data']:
                dog_image_url = giphy_response.json()['data'][0]['images']['original']['url']

            # Guardar búsqueda en la base de datos
            dog_breed = DogBreed.objects.create(
                name=dog_breed_name,
                description=dog_temperament,
                image_url=dog_image_url,
            )

            # Usar el serializer para devolver la respuesta
            serializer = DogBreedSerializer(dog_breed)
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "error": "Breed not found",
            "details": f"Could not find breed '{breed_name}' in external API"
        }, status=status.HTTP_404_NOT_FOUND)

    return Response({
        "error": "No breed specified",
        "details": "Please provide a breed name in the request body."
    }, status=status.HTTP_400_BAD_REQUEST)

filters_param = openapi.Parameter(
    'filter',
    openapi.IN_QUERY,
    description="Optional filter terms to search in breed names or descriptions (comma-separated)",
    type=openapi.TYPE_ARRAY,
    items=openapi.Items(type=openapi.TYPE_STRING),
    collection_format="multi"
)

@swagger_auto_schema(
    method='get',
    operation_description="Get a list of dog breeds. Optionally filter by terms.",
    manual_parameters=[filters_param],
    responses={200: "Success - List of breeds", 500: "Internal Server Error"}
)
@api_view(['GET'])

def get_dog_breeds(request):
    # Obtener los filtros opcionales desde la query string, si existen
    search_terms = request.GET.getlist('filter')

    # Revisamos si ya existe un cache para las razas
    cached_breeds = cache.get('dog_breeds')
    
    if cached_breeds is None:
        # Si no hay cache, obtenemos todas las razas de la API y las cacheamos
        response = requests.get(DOGS_API_URL)
        if response.status_code == 200:
            breeds = response.json()
            breed_names = [
                {'name': breed.get('name', 'Unknown breed'), 'description': breed.get('temperament', '')}
                for breed in breeds
            ]
            # Cacheamos todas las razas para futuras peticiones
            cache.set('dog_breeds', breed_names, timeout=86400)  # Cache por 24 horas
        else:
            return Response({"error": "Failed to fetch breeds from DogsAPI"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        # Si ya hay cache, usamos los datos cacheados
        breed_names = cached_breeds

    # Si hay filtros, aplicamos los filtros
    if search_terms:
        search_terms = [term.lower() for term in search_terms]  # Convertimos los términos a minúsculas
        
        # Filtramos las razas que contengan **todos** los términos de búsqueda en el nombre o la descripción
        breed_names = [
            breed for breed in breed_names
            if all(term in breed['name'].lower() or term in breed['description'].lower() for term in search_terms)
        ]
    
    # Extraemos solo los nombres de las razas, sin necesidad de otros atributos
    breed_names = [breed['name'] for breed in breed_names]
    
    return Response({
        "status": "success",
        "data": breed_names
    }, status=status.HTTP_200_OK)
    
@swagger_auto_schema(
    method='get',
    operation_description="Get the search history of dog breeds. Provide your JWT token prefixed with 'Bearer'",
    responses={
        200: "Success - List of search history",
        401: "Unauthorized - Invalid or missing token",
        403: "Forbidden - Admin access only"
    },
    security=[{'Bearer': []}] 
)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def user_search_history(request):

    searches = DogBreed.objects.all()
    

    # Filtrar por palabra clave en la descripción, si 'keyword' está presente en los parámetros de la query
    keyword = request.query_params.get('keyword', None)
    if keyword:
        searches = searches.filter(description__icontains=keyword)  # Filtrado no sensible a mayúsculas

    # Ordena por tiempo, más reciente primero
    searches = searches.order_by('-time')

    serializer = DogBreedHistorySerializer(searches, many=True)

    return Response({
        "status": "success",
        "data": serializer.data
        }, status=status.HTTP_200_OK)