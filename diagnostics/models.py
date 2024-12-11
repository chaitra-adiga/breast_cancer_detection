from django.db import models

class Diagnostic(models.Model):
    user_id = models.CharField(max_length=15, unique=True)  # Use phone number
    user_name = models.CharField(max_length=100)
    email_id = models.EmailField(max_length=100)
    user_phn = models.CharField(max_length=15)
    age = models.IntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status_of_prediction = models.CharField(max_length=100, default='Pending')

    def __str__(self):
        return f"{self.user_name}-{self.user_id}"  # bcd_2024

class Scan(models.Model):
    diagnostic = models.ForeignKey(Diagnostic, related_name='scans', on_delete=models.CASCADE)
    scan = models.ImageField(upload_to='scans/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Scan for {self.diagnostic.user_name} - {self.uploaded_at}"