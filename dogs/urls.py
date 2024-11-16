from django.urls import path
from . import views

urlpatterns = [
    # Endpoint para obtener las razas de perros
    path('breeds/', views.get_dog_breeds, name='get_dog_breeds'),  # GET para obtener razas

    # Endpoint para obtener detalles de una raza específica, también público
    path('', views.get_dog_info, name='get_dog_info'),  # POST para obtener detalles y la imagen

    # Endpoint para ver el historial de búsquedas, solo admin puede acceder
    path('search-history/', views.user_search_history, name='user_search_history'),  # Historial de búsquedas
]