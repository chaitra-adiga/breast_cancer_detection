from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.user_home, name='user_home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user-login'),
]