from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    name= forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(
        max_length=15,
        help_text='Enter your phone number. This will be used for login.'
    )
    
    class Meta:
        model = User
        fields = ['name','phone_number', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['phone_number']  # Use phone number as username
        if commit:
            user.save()
        return user

class UserLoginForm(forms.Form):
    phone_number = forms.CharField(
        max_length=15,
        label='Phone Number',
        help_text='Enter the phone number you registered with.'
    )
    password = forms.CharField(widget=forms.PasswordInput)