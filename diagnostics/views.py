from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .models import Diagnostic, Scan
from .forms import DiagnosticForm, ScanForm

def landing_page(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        login_type = request.POST.get('login_type')
        if login_type == 'diagnostic_admin':
            return redirect('diagnostic_login')
        elif login_type == 'user_profile':
            return redirect('user_login')
    return render(request, 'login.html')

def diagnostic_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:  # If credentials match
            if user.username == 'diagnostic_admin':  # Ensure it's the correct admin user
                login(request, user)
                return redirect('diagnostic_dashboard')
            else:
                return HttpResponse("Unauthorized user", status=403)
        else:  # Invalid credentials
            return render(request, 'login_diagnostics.html', {'error': 'Invalid credentials'})
    return render(request, 'login_diagnostics.html')

def user_login_view(request):
    # Implement user login logic here
    return render(request, 'user_login.html')

def diagnostic_dashboard_view(request):
    diagnostics = Diagnostic.objects.all()
    return render(request, 'diagnostic_dashboard.html', {'diagnostics': diagnostics})

def add_patient_view(request):
    if request.method == 'POST':
        form = DiagnosticForm(request.POST)
        if form.is_valid():
            diagnostic = form.save()
            return redirect('diagnostic_dashboard')
    else:
        form = DiagnosticForm()
    return render(request, 'add_patient.html', {'form': form})

def add_scan_view(request, user_id):
    diagnostic = get_object_or_404(Diagnostic, user_id=user_id)
    if request.method == 'POST':
        form = ScanForm(request.POST, request.FILES)
        if form.is_valid():
            scan = form.save(commit=False)
            scan.diagnostic = diagnostic
            scan.save()
            return redirect('diagnostic_dashboard')
    else:
        form = ScanForm()
    return render(request, 'add_scan.html', {'form': form, 'diagnostic': diagnostic})