from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('diagnostic-login/', views.diagnostic_login_view, name='diagnostic_login'),
    path('user-login/', views.user_login_view, name='user_login'),
    path('diagnostic-dashboard/', views.diagnostic_dashboard_view, name='diagnostic_dashboard'),
    path('add-patient/', views.add_patient_view, name='add_patient'),
    path('add-scan/<str:user_id>/', views.add_scan_view, name='add_scan'),
]