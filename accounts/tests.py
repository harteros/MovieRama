from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import TestCase


# Create your tests here.


class RegisterViewTest(TestCase):

    def test_register_view_load(self):
        """
            test if register view loads successfully
        """
        response = self.client.get("/accounts/register/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "<h2>Sign up</h2>", html=True)

    def test_register_success(self):
        """
            test if a valid registration redirects to the home page and creates a new user
        """
        form = {'first_name': "test", 'last_name': "test", 'email': "test@test.com", 'password1': "12345678!",
                'password2': "12345678!", 'username': "test"}
        response = self.client.post('/accounts/register/', data=form)

        self.assertRedirects(response, '/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        self.assertIn(User.objects.get(username="test"), User.objects.all())
