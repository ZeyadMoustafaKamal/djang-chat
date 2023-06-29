from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model, authenticate

from django import forms

from .models import UserProfile

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = 'email',

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = 'email', 
class CustomAuthenticationForm(AuthenticationForm):
    def clean(self):
        # I did not want to change the whole form so I will just change the valriables names
        email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if email is not None and password:
            self.user_cache = authenticate(
                self.request, email=email, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = 'user',
        widgets = {
            'bio': forms.Textarea(attrs={'placeholder': 'Enter the bio'}),
            } 


