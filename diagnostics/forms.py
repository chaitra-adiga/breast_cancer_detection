from django import forms
from .models import Diagnostic, Scan

class DiagnosticForm(forms.ModelForm):
    had_implants_before = forms.ChoiceField(
        choices=Diagnostic.YES_NO_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'radio-group'})
    )
    
    class Meta:
        model = Diagnostic
        fields = ['user_id', 'user_name', 'email_id', 'user_phn', 'age', 'had_implants_before', 'status_of_prediction']

class ScanForm(forms.ModelForm):
    type_of_scan = forms.ChoiceField(
        choices=Scan.SCAN_TYPE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'radio-group'})
    )
    view_of_scan = forms.ChoiceField(
        choices=Scan.VIEW_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'radio-group'})
    )
    
    class Meta:
        model = Scan
        fields = ['scan', 'type_of_scan', 'view_of_scan']