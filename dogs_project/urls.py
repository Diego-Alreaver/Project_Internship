from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.shortcuts import redirect

# Swagger Schema
schema_view = get_schema_view(
    openapi.Info(
        title="Dog API",
        default_version='v1',
        description="API to obtain dog races and images of them",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@dogapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('dogs.urls')),
    path('', lambda request: redirect('swagger/', permanent=False)),  # Redirects to swagger
    
    #JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    #Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]