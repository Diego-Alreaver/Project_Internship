from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    # Endpoint to get dogs breeds 
    path('breeds/', views.get_dog_breeds, name='get_dog_breeds'),

    # Endpoint to get details and gif on a specific dog 
    path('breeds/details/', views.fetch_breed_details, name='fetch_breed_details'), 

    # Endpoint to see search history, only accessible to admin 
    path('search-history/', views.user_search_history, name='user_search_history'), 

    # Endpoint to delete search history, only accessible to admin
    path('search-history/delete/', views.delete_all_searches, name='delete_all_searches'),

    path("webpage", TemplateView.as_view(template_name="index.html"), name="home"), 
]