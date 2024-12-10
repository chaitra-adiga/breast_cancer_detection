from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

def login_view(request):
    if request.method == 'POST':
        login_type = request.POST.get('login_type')
        if login_type == 'diagnostic_admin':
            return redirect('diagnostic_login')
        elif login_type == 'user_profile':
            return redirect('user_login')
    return render(request, 'diagnostics/login.html')

def diagnostic_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:  # If credentials match
            if user.username == 'diagnostic_admin':  # Ensure it's the correct admin user
                login(request, user)
                return redirect('dashboard')
            else:
                return HttpResponse("Unauthorized user", status=403)
        else:  # Invalid credentials
            return render(request, 'diagnostics/login_diagnostics.html', {'error': 'Invalid credentials'})
    return render(request, 'diagnostics/login_diagnostics.html')

def user_login_view(request):
    # Implement user login logic here
    return render(request, 'diagnostics/user_login.html')