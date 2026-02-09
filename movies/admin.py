from django.contrib import admin
from .models import Movie

# Register your models here.

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'director', 'genre', 'year', 'rating', 'duration', 'created_at']
    list_filter = ['genre', 'year']
    search_fields = ['title', 'director', 'genre']
    ordering = ['-created_at']

