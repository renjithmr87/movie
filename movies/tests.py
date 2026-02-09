from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Movie

# Create your tests here.

class MovieModelTest(TestCase):
    """Test cases for Movie model"""
    
    def setUp(self):
        """Create a test movie"""
        self.movie = Movie.objects.create(
            title="Test Movie",
            director="Test Director",
            genre="Action",
            year=2024,
            rating=8.5,
            duration=120,
            description="Test description"
        )
    
    def test_movie_creation(self):
        """Test that a movie can be created"""
        self.assertEqual(self.movie.title, "Test Movie")
        self.assertEqual(self.movie.director, "Test Director")
        self.assertEqual(self.movie.year, 2024)
    
    def test_movie_str(self):
        """Test the string representation of a movie"""
        self.assertEqual(str(self.movie), "Test Movie (2024)")


class MovieAPITest(APITestCase):
    """Test cases for Movie REST API"""
    
    def setUp(self):
        """Create test movies"""
        self.movie1 = Movie.objects.create(
            title="Movie 1",
            director="Director 1",
            genre="Drama",
            year=2023,
            rating=7.5,
            duration=100
        )
        self.movie2 = Movie.objects.create(
            title="Movie 2",
            director="Director 2",
            genre="Comedy",
            year=2024,
            rating=8.0,
            duration=110
        )
    
    def test_get_all_movies(self):
        """Test retrieving all movies"""
        url = reverse('movie-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_get_single_movie(self):
        """Test retrieving a single movie"""
        url = reverse('movie-detail', kwargs={'pk': self.movie1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Movie 1')
    
    def test_create_movie(self):
        """Test creating a new movie"""
        url = reverse('movie-list')
        data = {
            'title': 'New Movie',
            'director': 'New Director',
            'genre': 'Thriller',
            'year': 2024,
            'rating': 9.0,
            'duration': 130
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.count(), 3)
        self.assertEqual(Movie.objects.latest('id').title, 'New Movie')
    
    def test_update_movie(self):
        """Test updating a movie"""
        url = reverse('movie-detail', kwargs={'pk': self.movie1.pk})
        data = {
            'title': 'Updated Movie',
            'director': 'Updated Director',
            'genre': 'Drama',
            'year': 2023,
            'rating': 8.5,
            'duration': 100
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.movie1.refresh_from_db()
        self.assertEqual(self.movie1.title, 'Updated Movie')
    
    def test_delete_movie(self):
        """Test deleting a movie"""
        url = reverse('movie-detail', kwargs={'pk': self.movie1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Movie.objects.count(), 1)


class MovieViewTest(TestCase):
    """Test cases for Movie web views"""
    
    def setUp(self):
        """Create a test movie"""
        self.movie = Movie.objects.create(
            title="Web Test Movie",
            director="Web Director",
            genre="Action",
            year=2024,
            rating=8.0,
            duration=120
        )
    
    def test_movie_list_view(self):
        """Test the movie list view"""
        url = reverse('movie_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Web Test Movie')
    
    def test_movie_detail_view(self):
        """Test the movie detail view"""
        url = reverse('movie_detail', kwargs={'pk': self.movie.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Web Test Movie')
        self.assertContains(response, 'Web Director')

