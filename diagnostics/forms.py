from django import forms
from .models import Diagnostic, Scan

class DiagnosticForm(forms.ModelForm):
    class Meta:
        model = Diagnostic
        fields = ['user_id', 'user_name', 'email_id', 'user_phn', 'age', 'status_of_prediction']

class ScanForm(forms.ModelForm):
    class Meta:
        model = Scan
        fields = ['scan']