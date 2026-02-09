from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Movie
from .serializers import MovieSerializer

# Create your views here.

class MovieViewSet(viewsets.ModelViewSet):
    """
    API ViewSet for CRUD operations on Movie model
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


# Traditional Django views for web interface
def movie_list(request):
    """
    List all movies
    """
    movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', {'movies': movies})


def movie_detail(request, pk):
    """
    Display details of a single movie
    """
    movie = get_object_or_404(Movie, pk=pk)
    return render(request, 'movies/movie_detail.html', {'movie': movie})


def movie_create(request):
    """
    Create a new movie
    """
    if request.method == 'POST':
        movie = Movie(
            title=request.POST.get('title'),
            director=request.POST.get('director'),
            genre=request.POST.get('genre'),
            year=request.POST.get('year'),
            description=request.POST.get('description', ''),
            rating=request.POST.get('rating', 0.0),
            duration=request.POST.get('duration')
        )
        movie.save()
        return redirect('movie_list')
    return render(request, 'movies/movie_form.html')


def movie_update(request, pk):
    """
    Update an existing movie
    """
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        movie.title = request.POST.get('title')
        movie.director = request.POST.get('director')
        movie.genre = request.POST.get('genre')
        movie.year = request.POST.get('year')
        movie.description = request.POST.get('description', '')
        movie.rating = request.POST.get('rating', 0.0)
        movie.duration = request.POST.get('duration')
        movie.save()
        return redirect('movie_detail', pk=pk)
    return render(request, 'movies/movie_form.html', {'movie': movie})


def movie_delete(request, pk):
    """
    Delete a movie
    """
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        movie.delete()
        return redirect('movie_list')
    return render(request, 'movies/movie_confirm_delete.html', {'movie': movie})

