from django.db import models
from django.contrib.auth.models import User

class Diagnostic(models.Model):
    YES_NO_CHOICES = [
        (1, 'Yes'),
        (0, 'No'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)  # Add this line
    user_identity = models.CharField(max_length=15, unique=True)  # Use phone number
    user_name = models.CharField(max_length=100)
    email_id = models.EmailField(max_length=100)
    user_phn = models.CharField(max_length=15)
    age = models.IntegerField()
    had_implants_before = models.IntegerField(
        choices=YES_NO_CHOICES,
        default=0  #Default to No
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status_of_prediction = models.CharField(max_length=100, default='Pending')

    def __str__(self):
        return f"{self.user_name}-{self.user_identity}"  # bcd_2024

class Scan(models.Model):
    SCAN_TYPE_CHOICES = [
        (1, 'MLO'),
        (0, 'CC'),
    ]
    VIEW_CHOICES = [
        (1, 'Left'),
        (0, 'Right'),
    ]
    diagnostic = models.ForeignKey(Diagnostic, related_name='scans', on_delete=models.CASCADE)
    scan = models.ImageField(upload_to='scans/')
    type_of_scan = models.IntegerField(
        choices=SCAN_TYPE_CHOICES,
        default=1 #default to MLO
    )
    view_of_scan = models.IntegerField(
        choices=VIEW_CHOICES,
        default=1 #Default to Left
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Scan for {self.diagnostic.user_name} - {self.uploaded_at}"