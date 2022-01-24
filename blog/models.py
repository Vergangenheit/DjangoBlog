from django.db import models
from django.db.models import CharField
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):

    title = models.CharField(max_length=100, null=False)
    date_posted = models.DateTimeField(auto_now_add=True, null=False)
    content = models.TextField(null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> CharField:
        return self.title
