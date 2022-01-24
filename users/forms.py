from django import forms
from django.contrib.auth.models import User
from django.db.models import QuerySet
from typing import Optional


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required',
                             error_messages={'required': 'Sorry, you will need an email'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('user_name', 'email',)

    def clean_username(self) -> Optional[str]:
        user_name: str = self.cleaned_data['user_name'].lower()
        r: QuerySet = User.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError("Username already exist")
        return user_name

    def clean_email(self) -> Optional[str]:
        email: str = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, that is already taken')
        return email
