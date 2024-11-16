import os
from dotenv import load_dotenv
import requests

from django.core.cache import cache

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import DogBreed
from .serializers import DogBreedSerializer, DogBreedHistorySerializer

load_dotenv() # get sensible data from .env
GIPHY_API_KEY = os.getenv('GIPHY_API_KEY')
DOGS_API_URL = "https://api.thedogapi.com/v1/breeds"




# Define expected parameter on POST
breed_param = openapi.Parameter(
    'breed',
    openapi.IN_BODY,
    description="Breed name to fetch details and image",
    type=openapi.TYPE_STRING
)
@swagger_auto_schema(
    method='post',
    operation_description="Fetch dog breed details from thedogapi and a gif of that breed from Giphy.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'breed': openapi.Schema(type=openapi.TYPE_STRING, description='Dog breed name')
        },
        required=['breed']
    ),
    responses={
        200: "Success - Returns details and gif of the dog breed",
        400: "Bad Request - Breed not specified",
        404: "Not Found - Breed not found in external API"
    }
)
# I chose @api_view (function-based) instead of APIVIEW (class-based) to keep it simple as this is a small project
@api_view(['POST'])
def fetch_breed_details(request):
    breed_name = request.data.get('breed', '')

    if breed_name:
        dog_api_url = f"https://api.thedogapi.com/v1/breeds/search?q={breed_name}" # get breed info from thedogapi API
        response = requests.get(dog_api_url)

        if response.status_code == 200 and response.json():
            dog_data = response.json()[0]
            dog_breed_name = dog_data.get('name', 'No name available')
            dog_temperament = dog_data.get('temperament', 'No temperament information available')

            giphy_url = f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_API_KEY}&q={breed_name}&limit=1" # get gif from giphy API
            giphy_response = requests.get(giphy_url)

            dog_image_url = "No image available"
            if giphy_response.status_code == 200 and giphy_response.json()['data']:
                dog_image_url = giphy_response.json()['data'][0]['images']['original']['url']

            # Save user search to database in case admin wants that info
            dog_breed = DogBreed.objects.create(
                name=dog_breed_name,
                description=dog_temperament,
                image_url=dog_image_url,
            )

            # Serialize the successful response
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




filters_param = openapi.Parameter( # adds the option on swagger to include a filter or filters
    'filter',
    openapi.IN_QUERY,
    description="Optional filter terms to search in breed names or descriptions (comma-separated)",
    type=openapi.TYPE_ARRAY,
    items=openapi.Items(type=openapi.TYPE_STRING),
    collection_format="multi"
)
@swagger_auto_schema(
    method='get',
    operation_description="Get a list of dog breeds from thedogapi. Optionally filter by terms.",
    manual_parameters=[filters_param],
    responses={200: "Success - List of breeds", 500: "Internal Server Error"}
)
@api_view(['GET'])
def get_dog_breeds(request):
    search_terms = request.GET.getlist('filter')

    # Check if there is already a cache for breeds to optimize API calls
    cached_breeds = cache.get('dog_breeds')
    
    if cached_breeds is None: # Do the API call if there is no cache
        response = requests.get(DOGS_API_URL)
        if response.status_code == 200:
            breeds = response.json()
            breed_names = [
                {'name': breed.get('name', 'Unknown breed'), 'description': breed.get('temperament', '')}
                for breed in breeds
            ]
            # Cache all the breeds for future request
            cache.set('dog_breeds', breed_names, timeout=86400)  # Cache for 24 hours, since I assume we don't get new dog breeds every hour
        else:
            return Response({"error": "Failed to fetch breeds from DogsAPI"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        breed_names = cached_breeds # If there is already a cache we use that data instead

    # Apply filters if there is any
    if search_terms:
        search_terms = [term.lower() for term in search_terms] 
        breed_names = [
            breed for breed in breed_names
            if all(term in breed['name'].lower() or term in breed['description'].lower() for term in search_terms)
        ]
    
    # We only want the name of the breeds that have these specific traits
    breed_names = [breed['name'] for breed in breed_names]
    
    return Response({
        "status": "success",
        "data": breed_names,
    }, status=status.HTTP_200_OK)




@swagger_auto_schema(
    method='get',
    operation_description="Get the search history of dog breeds. Only accessible for admin. Provide your JWT token prefixed with 'Bearer'",
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
    
    # Filter by keyword in the description, if 'keyword' is present in the query parameters
    keyword = request.query_params.get('keyword', None)
    if keyword:
        searches = searches.filter(description__icontains=keyword) 

    # Sort by time, newest first
    searches = searches.order_by('-time')

    serializer = DogBreedHistorySerializer(searches, many=True)

    return Response({
        "status": "success",
        "data": serializer.data
        }, status=status.HTTP_200_OK)




@swagger_auto_schema(
    method='delete',
    operation_description="Deletes all the search history of dog breeds. Only accessible for admin. Provide your JWT token prefixed with 'Bearer'",
    responses={
        204: "No content - Deleted search history",
        401: "Unauthorized - Invalid or missing token",
        403: "Forbidden - Admin access only"
    },
    security=[{'Bearer': []}] 
)
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_all_searches(request):
    try:
        DogBreed.objects.all().delete()
        return Response({
            "status": "success",
            "message": "All search history has been deleted."
        }, status=status.HTTP_204_NO_CONTENT)
    
    except Exception as e:
        return Response({
            "status": "error",
            "message": f"An error occurred while deleting records: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)