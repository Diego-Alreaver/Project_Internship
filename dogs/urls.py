from django.urls import path
from . import views

urlpatterns = [
    # Endpoint to get dogs breeds 
    path('breeds/', views.get_dog_breeds, name='get_dog_breeds'),

    # Endpoint to get details and gif on a specific dog 
    path('breeds/details/', views.fetch_breed_details, name='fetch_breed_details'), 

    # Endpoint to see search history, only accessible to admin 
    path('search-history/', views.user_search_history, name='user_search_history'),  
]