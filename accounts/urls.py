from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomAuthenticationForm

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(form_class=CustomAuthenticationForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('confirm_token/', views.ConfirmTokenView.as_view(), name='confirm_token'),
    path('confirm_email/', views.EmailConfirmationView.as_view(), name='confirm_email'),
    path('profile/', views.ProfileView.as_view(), name='profile')
]