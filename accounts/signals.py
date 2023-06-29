from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.db import transaction

import random
import string

from .models import UserProfile

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_handler(created, instance, *args, **kwargs):
    if created:
        
        if not instance.username:
            base_username = instance.email.split('@')[0]
            username = base_username
            while User.objects.filter(username=username):
                suffix = ''.join(random.choices(string.digits, k=4))
                username = f'{base_username}-{suffix}'
            instance.username = username
            # if there is any errors it will not be commited
            transaction.on_commit(lambda : instance.save())
        
        UserProfile.objects.create(user=instance) # create a userprofile instance
