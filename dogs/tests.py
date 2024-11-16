from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class FetchBreedDetailsTest(APITestCase):

    def test_fetch_valid_breed_details(self): # Success (200) if breed is valid
        url = reverse('fetch_breed_details')
        data = {"breed": "Akita"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", response.data) 

    def test_fetch_invalid_breed(self): # 404 not found if breed is invalid
        url = reverse('fetch_breed_details')
        data = {"breed": "Siamese"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_missing_breed_field(self): # required field "breed" not included on endpoint call
        url = reverse('fetch_breed_details')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class GetDogBreedsTest(APITestCase):

    def test_fetch_all_breeds(self): # Success if response 200 and list is not empty
        url = reverse('get_dog_breeds')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0) 


from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class UserSearchHistoryTest(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin', password='admin')
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_access_search_history(self): # Success if token is valid
        url = reverse('user_search_history')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_access(self): # 401 if token is invalid, user unauthorized
        self.client.credentials()  
        url = reverse('user_search_history')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)