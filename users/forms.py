from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models import QuerySet
from typing import Optional


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(label="Enter Email")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


