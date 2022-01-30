from django.db import models
from django.contrib.auth.admin import User
from django.utils.translation import gettext_lazy as _
from PIL import Image as image
from PIL.Image import Image


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    email = models.EmailField(_('email_address'), unique=True)
    avatar = models.ImageField(upload_to="users/static/profile_pics/", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.user.username} Profile'

    def save(self):
        super().save()
        img: Image = image.open(self.avatar.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.avatar.path)
