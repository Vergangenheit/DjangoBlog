from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from .forms import RegisterForm


# Create your views here.
def register(request: HttpRequest):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect("/home")
    else:
        form = RegisterForm()

    return render(request, "users/register.html", {"form": form})
