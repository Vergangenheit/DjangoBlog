from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.db.models import QuerySet
from .models import Post
from django.core.paginator import Paginator, Page
from django.views.generic import ListView


# Create your views here.

def home(request: HttpRequest) -> HttpResponse:
    # grab all the posts
    posts: QuerySet = Post.objects.all()
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj: Page = paginator.get_page(page_number)
    return render(request, 'blog/home.html', {'page_obj': page_obj})


def about(request: HttpRequest) -> HttpResponse:
    return render(request, 'blog/about.html', {'title': 'About'})


class PostListView(ListView):
    paginate_by = 5
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
