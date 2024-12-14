from django.db import models

class Diagnostic(models.Model):
    YES_NO_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    user_id = models.CharField(max_length=15, unique=True)  # Use phone number
    user_name = models.CharField(max_length=100)
    email_id = models.EmailField(max_length=100)
    user_phn = models.CharField(max_length=15)
    age = models.IntegerField()
    #had_implants_before = models.BooleanField(default=False)
    had_implants_before = models.CharField(
        max_length=3,
        choices=YES_NO_CHOICES,
        default='No'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status_of_prediction = models.CharField(max_length=100, default='Pending')

    def __str__(self):
        return f"{self.user_name}-{self.user_id}"  # bcd_2024

class Scan(models.Model):
    SCAN_TYPE_CHOICES = [
        ('MLO', 'MLO'),
        ('CC', 'CC'),
    ]
    VIEW_CHOICES = [
        ('Left', 'Left'),
        ('Right', 'Right'),
    ]
    diagnostic = models.ForeignKey(Diagnostic, related_name='scans', on_delete=models.CASCADE)
    scan = models.ImageField(upload_to='scans/')
    type_of_scan = models.CharField(
        max_length=3,
        choices=SCAN_TYPE_CHOICES,
        default='MLO'
    )
    view_of_scan = models.CharField(
        max_length=5,
        choices=VIEW_CHOICES,
        default='Left'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Scan for {self.diagnostic.user_name} - {self.uploaded_at}"