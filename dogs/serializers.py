from rest_framework import serializers
from .models import DogBreed
from rest_framework import serializers

class DogBreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = DogBreed
        fields = ['name', 'description', 'image_url']

class DogBreedHistorySerializer(DogBreedSerializer):
    time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta(DogBreedSerializer.Meta):
        fields = DogBreedSerializer.Meta.fields + ['time']

