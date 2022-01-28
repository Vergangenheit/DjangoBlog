from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from .forms import RegisterForm
from typing import Union
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError


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


def password_reset_request(request: HttpRequest) -> Union[
    HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect]:
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data: str = password_reset_form.cleaned_data['email']
            associated_users: QuerySet = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "users/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email: str = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    # messages.success(request, "A message with reset password instructions has been sent to your inbox.")
                    return redirect("password_reset_done")
            else:
                messages.error(request, 'An invalid email has been entered.')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="users/password_reset.html",
                  context={'password_reset_form': password_reset_form})
