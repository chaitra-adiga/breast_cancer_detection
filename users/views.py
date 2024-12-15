from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .forms import UserRegisterForm, UserLoginForm
from diagnostics.models import Diagnostic  # Add this import statement

def user_home(request):
    # Logic to determine the user status
    # For example, status could be 'uploaded', 'processing', or 'completed'
    status = 'processing'  # Replace with actual logic
    return render(request, 'users/home.html', {'status': status})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('phone_number')
            try:
                diagnostic = Diagnostic.objects.get(user_phn=phone_number)
            except Diagnostic.DoesNotExist:
                return render(request, 'users/waiting.html')  # Redirect to waiting page
            user = form.save()
            diagnostic.user = user  # Link the Diagnostic to the User
            diagnostic.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('user-login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('phone_number')
            password = form.cleaned_data.get('password')
            user = authenticate(username=phone_number, password=password)
            if user:
                login(request, user)
                return redirect('user_home')  # Redirect to user dashboard or appropriate page
            else:
                messages.error(request, 'Invalid phone number or password')
    else:
        form = UserLoginForm()
    return render(request, 'users/user_login.html', {'form': form})