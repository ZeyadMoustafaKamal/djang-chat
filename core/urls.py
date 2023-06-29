from django.urls import path

from .import views
urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('user/<str:user_name>/', views.user_profile, name='user_profile')
]
