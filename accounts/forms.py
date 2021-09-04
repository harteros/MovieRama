from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    """
        A sign up form requiring all :model:`auth.User` info fields
    """
    first_name = forms.CharField(max_length=100, help_text='Required')
    last_name = forms.CharField(max_length=100, help_text='Required')
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
