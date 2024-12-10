from django.db import models

class Diagnostic(models.Model):
    #this class is for adding patients 
    patient_id = models.CharField(max_length=15, unique=True)  # Use phone number
    patient_name = models.CharField(max_length=100)
    email_id=models.EmailField(max_length=100)
    patient_phn=models.CharField(max_length=15)
    age = models.IntegerField()
    scan = models.ImageField(upload_to='scans/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.patient_name}-{self.patient_id}" #bcd_2024
    