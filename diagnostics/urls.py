from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('diagnostic-login/', views.diagnostic_login_view, name='diagnostic_login'),
    path('user-login/', views.user_login_view, name='user_login'),
    path('diagnostic-dashboard/', views.DiagnosticListView.as_view(), name='diagnostic_dashboard'),
    path('add-patient/', views.DiagnosticCreateView.as_view(), name='add_patient'),
    path('add-scan/<str:user_id>/', views.ScanCreateView.as_view(), name='add_scan'),
    path('add-scan-existing/', views.AddScanForExistingPatientView.as_view(), name='add_scan_existing'),
    path('update-scan/<int:pk>/', views.ScanUpdateView.as_view(), name='update_scan'),
    path('delete-scan/<int:pk>/', views.ScanDeleteView.as_view(), name='delete_scan'),
    path('diagnostic/<int:pk>/', views.DiagnosticDetailView.as_view(), name='diagnostic_detail'),
    path('diagnostic/<int:pk>/update/', views.DiagnosticUpdateView.as_view(), name='diagnostic_update'),
    path('diagnostic/<int:pk>/delete/', views.DiagnosticDeleteView.as_view(), name='diagnostic_delete'),
    path('patient-not-found/', TemplateView.as_view(template_name='diagnostics/patient_not_found.html'), name='patient_not_found'),
]