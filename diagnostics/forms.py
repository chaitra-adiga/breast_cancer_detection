from django import forms
from .models import Diagnostic

class DiagnosticForm(forms.ModelForm):
    class Meta:
        model = Diagnostic
        fields = ['user_id', 'user_name', 'email_id', 'user_phn', 'age', 'scan']