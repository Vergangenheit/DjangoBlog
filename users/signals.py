from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile
from typing import Dict, Optional


@receiver(post_save, sender=User)
def create_profile(sender: User, instance: User, created: bool, **kwargs: Optional[Dict]):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender: User, instance: User, **kwargs: Optional[Dict]):
    instance.profile.save()
