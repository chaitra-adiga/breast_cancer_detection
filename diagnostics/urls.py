from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('diagnostic-login/', views.diagnostic_login_view, name='diagnostic_login'),
    path('user-login/', views.user_login_view, name='user_login'),
]