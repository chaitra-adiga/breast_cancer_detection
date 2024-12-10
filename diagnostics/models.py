from django.db import models

class Diagnostic(models.Model):
    # this class is for adding patients/user 
    user_id = models.CharField(max_length=15, unique=True)  # Use phone number
    user_name = models.CharField(max_length=100)
    email_id = models.EmailField(max_length=100)
    user_phn = models.CharField(max_length=15)
    age = models.IntegerField()
    scan = models.ImageField(upload_to='scans/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status_of_prediction = models.CharField(max_length=100, default='Pending')

    def __str__(self):
        return f"{self.user_name}-{self.user_id}"  # bcd_2024