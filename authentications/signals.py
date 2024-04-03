from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *


@receiver(post_save, sender = User)
def UpdateProfile(sender, instance, created, **kwargs):
    if created:
        created = User.objects.get_or_create(account = instance)