from django.db import models


class DogBreed(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)  # Almacena la fecha y hora de la búsqueda

    def __str__(self):
        return self.name