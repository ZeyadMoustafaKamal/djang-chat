from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _


class CustomUserManager(BaseUserManager):
    """ Create and save a user object """
    def create_user(self, email, password, **extrafields):
        if not email:
            raise ValueError(_("The Email must be set"))

        email = self.normalize_email(email)
        user = self.model(email=email, **extrafields)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self, email, password, **kwargs):
        """ Create and save a superuser object"""
        email = self.normalize_email(email)

        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError(_('Is staff must be true'))
        if kwargs.get('is_superuser') is not True:
            raise ValueError(_('Is superuser must be true'))
        
        return self.create_user(email,password, **kwargs)


