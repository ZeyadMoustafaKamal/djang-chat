from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from .models import UserToken

def send_confirmation_email(user, request):
    # delete any token related to this user if any
    current_tokens = UserToken.objects.filter(user=user)
    if current_tokens.exists():
        current_tokens.delete()
    new_token = UserToken.objects.create(user=user)
    new_token.save()
    current_site = get_current_site(request)

    subject = 'Please confirm your email'
    message = f'Please visit this URL in order to confirm your email :\n http://{current_site}{reverse("confirm_token")}?token={new_token.secret_token}'
    recipient_list = [user.email]
    from_email = 'noreply@djangochat.com'
    send_mail(subject=subject, message=message, recipient_list=recipient_list, from_email=from_email)

