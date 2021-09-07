from datetime import datetime
from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from movies.models import Movie


class MoviesViewTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='test', password='12345678!')
        self.test_user2 = User.objects.create_user(username='test2', password='12345678!')
        self.test_user.save()
        self.test_user2.save()

        self.test_movie = Movie(title="title1", desc="desc", pub_date=datetime.now(), user=self.test_user)
        self.test_movie2 = Movie(title="title2", desc="desc", pub_date=datetime.now(), user=self.test_user2)
        self.test_movie.save()
        self.test_movie2.save()

        self.client.login(username='test', password='12345678!')

    def test_like_unlike_movie(self):
        """
            test a successful like and unlike of movie
        """
        data = {"movie_id": self.test_movie2.id, "like_btn": True}
        response = self.client.post('/react/', data=data)
        self.assertIn(self.test_user, Movie.objects.get(pk=self.test_movie2.id).likes.all())
        self.assertRedirects(response, '/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        response = self.client.post('/react/', data=data)
        self.assertNotIn(self.test_user, Movie.objects.get(pk=self.test_movie2.id).likes.all())
        self.assertRedirects(response, '/', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_react_to_own_movie(self):
        """
            test that a user cannot react to his own movie
        """
        data = {"movie_id": self.test_movie.id, "like_btn": True}
        response = self.client.post('/react/', data=data)
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

    def test_add_movie_view(self):
        """
            test if add movie view loads successfully
        """

        response = self.client.get("/add/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "<title>Add Movie</title>", html=True)

    def test_add_movie_success(self):
        """
            test if a movie creation redirects to the home page and creates a new movie
        """

        movie = {'title': "dummy", 'desc': "test", "user": self.test_user}
        response = self.client.post('/add/', data=movie)

        self.assertRedirects(response, '/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)
        self.assertIn(Movie.objects.get(title="dummy"), Movie.objects.all())
