from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from django.utils.translation import gettext as _
from django.utils import timezone
from django.urls import reverse

from .managers import CustomUserManager
from .fields import RandomField

import string
from datetime import timedelta


class CustomUser(AbstractBaseUser, PermissionsMixin):

    id = RandomField(available_chars=string.digits, length=8, max_length=10, primary_key=True)

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        null=True,
        blank=True,
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_("email address"), unique=True)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    def get_absolute_url(self):
        return reverse("user_profile", kwargs={"user_name": f'@{self.username}'})

class UserToken(models.Model):
    # The user the should use this token to verify his email
    # I will use the foreignkey instead of the one to one field to just avoid the errors
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='verification_token')

    # The actual token
    secret_token = RandomField(available_chars=string.digits + string.ascii_letters, length=40, max_length=40)

    # The time when the token is created
    time_created = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        # Every token should be valid for 3 hours only
        return timezone.now() - self.time_created < timedelta(hours=3)

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    picture = models.ImageField(upload_to='profile_images', default='profile_images/default.png')
    bio = models.TextField(blank=True)
    display_name = models.CharField(max_length=70, null=True, blank=True) # This is just to allow users to create the same name as other users so just give them some freedom

    def save(self, *args, **kwargs):
        if not self.display_name:
            self.display_name = self.user.username
        return super().save()
    
    


