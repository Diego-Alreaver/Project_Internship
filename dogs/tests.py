from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class FetchBreedDetailsTest(APITestCase):

    def test_fetch_valid_breed_details(self):
        url = reverse('fetch_breed_details')
        data = {"breed": "Akita"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", response.data)  # Verifica que la respuesta contiene información de la raza

    def test_fetch_invalid_breed(self):
        url = reverse('fetch_breed_details')
        data = {"breed": "Nonexistent Breed"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_missing_breed_field(self):
        url = reverse('fetch_breed_details')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class GetDogBreedsTest(APITestCase):

    def test_fetch_all_breeds(self):
        url = reverse('get_dog_breeds')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)  # Verifica que se devuelven razas

    def test_fetch_breeds_with_filter(self):
        url = reverse('get_dog_breeds')
        response = self.client.get(url, {'filter': 'shepherd'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all('shepherd' in breed.lower() for breed in response.data))

from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

class UserSearchHistoryTest(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin', password='admin123')
        self.token = Token.objects.create(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_access_search_history(self):
        url = reverse('user_search_history')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_access(self):
        self.client.credentials()  # Elimina el token de autorización
        url = reverse('user_search_history')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)