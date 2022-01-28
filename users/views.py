from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from .forms import RegisterForm
from typing import Union
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User


# Create your views here.
def register(request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username: str = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')

        return redirect('blog-home')
    else:
        form = RegisterForm()

    return render(request, "users/register.html", {"form": form})


def login_request(request: HttpRequest) -> Union[HttpResponseRedirect, HttpResponse]:
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username: str = form.cleaned_data.get('username')
            password: str = form.cleaned_data.get('password')
            user: User = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("blog-home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    form = AuthenticationForm()

    return render(request=request, template_name="users/login.html", context={'form': form})


def logout_request(request: HttpRequest) -> Union[HttpResponseRedirect, HttpResponsePermanentRedirect]:
    logout(request)
    messages.info(request, "You have succesfully logged out.")
    return redirect("blog-home")
