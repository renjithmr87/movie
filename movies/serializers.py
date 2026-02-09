from rest_framework import serializers
from .models import Movie


class MovieSerializer(serializers.ModelSerializer):
    """
    Serializer for Movie model
    """
    class Meta:
        model = Movie
        fields = ['id', 'title', 'director', 'genre', 'year', 'description', 
                  'rating', 'duration', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
