from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.http import HttpResponse
from .models import Diagnostic, Scan
from .forms import DiagnosticForm, ScanForm

def landing_page(request):
    return render(request, 'index.html')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    else:
        return redirect('landing_page')

def login_view(request):
    if request.method == 'POST':
        login_type = request.POST.get('login_type')
        if login_type == 'diagnostic_admin':
            return redirect('diagnostic_login')
        elif login_type == 'user_profile':
            return redirect('user-login')
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

class DiagnosticListView(ListView):
    model = Diagnostic
    template_name = 'diagnostic_dashboard.html'
    context_object_name = 'diagnostics'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Diagnostic.objects.filter(user_name__icontains=query) | Diagnostic.objects.filter(user_identity__icontains=query)
        return Diagnostic.objects.all()
    
    
class DiagnosticDetailView(LoginRequiredMixin, DetailView):
    model = Diagnostic
    template_name = 'diagnostic_detail.html'
    context_object_name = 'diagnostic'

class DiagnosticCreateView(LoginRequiredMixin, CreateView):
    model = Diagnostic
    form_class = DiagnosticForm
    template_name = 'add_patient.html'
    success_url = '/diagnostic-dashboard/'

class DiagnosticUpdateView(LoginRequiredMixin, UpdateView):
    model = Diagnostic
    form_class = DiagnosticForm
    template_name = 'diagnostic_form.html'
    success_url = '/diagnostic-dashboard/'

class DiagnosticDeleteView(LoginRequiredMixin, DeleteView):
    model = Diagnostic
    success_url = '/diagnostic-dashboard/'
    template_name = 'diagnostic_confirm_delete.html'

class ScanCreateView(LoginRequiredMixin, CreateView):
    model = Scan
    form_class = ScanForm
    template_name = 'add_scan.html'

    def form_valid(self, form):
        form.instance.diagnostic = get_object_or_404(Diagnostic, user_identity=self.kwargs['user_identity'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['diagnostic'] = get_object_or_404(Diagnostic, user_identity=self.kwargs['user_identity'])
        return context

    def get_success_url(self):
        return '/diagnostic-dashboard/'

class ScanUpdateView(LoginRequiredMixin, UpdateView):
    model = Scan
    form_class = ScanForm
    template_name = 'update_scan.html'
    success_url = '/diagnostic-dashboard/'

class ScanDeleteView(LoginRequiredMixin, DeleteView):
    model = Scan
    template_name = 'confirm_delete_scan.html'
    success_url = '/diagnostic-dashboard/'


class AddScanForExistingPatientView(LoginRequiredMixin, CreateView):
    model = Scan
    form_class = ScanForm
    template_name = 'add_scan_existing_patient.html'

    def form_valid(self, form):
        user_identity = self.request.POST.get('user_identity')
        try:
            diagnostic = Diagnostic.objects.get(user_identity=user_identity)
            form.instance.diagnostic = diagnostic
            return super().form_valid(form)
        except Diagnostic.DoesNotExist:
            return redirect('patient_not_found')

    def get_success_url(self):
        return '/diagnostic-dashboard/'