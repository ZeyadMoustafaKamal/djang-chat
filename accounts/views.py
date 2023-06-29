from typing import Any
from django.urls import reverse_lazy
from django.views.generic import CreateView, RedirectView, TemplateView, UpdateView
from django.contrib.auth import get_user_model
from django.db import transaction
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

from .forms import CustomUserCreationForm, ProfileForm
from .models import UserToken, UserProfile
from .utils import send_confirmation_email

User = get_user_model()

class SignUpView(CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('confirm_email')

    @transaction.atomic
    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        send_confirmation_email(user, self.request)
        return response

class ConfirmTokenView(RedirectView):
    """ The view that should ensure that the token is valid and redirect the user to the home page"""
    url = reverse_lazy('confirm_email')

    def get(self, request, *args, **kwargs):
        url = self.get_redirect_url()
        token = request.GET.get('token')
        user_token = UserToken.objects.filter(secret_token=token).first()
        if user_token:
            if user_token.is_valid():
                user_to_varify = user_token.user
                user_to_varify.is_active = True
                user_to_varify.save()
                # The user should go to the login page and login again so I will have to execute the login function here                
        return HttpResponseRedirect(url)

class EmailConfirmationView(TemplateView):
    """ The user will be redirected to this view and in here he can request another token to send """
    template_name = 'registration/email_confirmation.html'

class ProfileView(UpdateView):
    form_class = ProfileForm
    template_name = 'registration/profile.html'
    model = UserProfile
    success_url = reverse_lazy('profile')


    def get_object(self):
        user_profile = UserProfile.objects.filter(user=self.request.user).first()
        return user_profile
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().post(request, *args, **kwargs)
    def form_valid(self, form: Any) -> HttpResponse:
        print(form.cleaned_data)
        return super().form_valid(form)