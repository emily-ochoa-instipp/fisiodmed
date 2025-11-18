from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def dashboard_analytics(request):
    return render(request, 'dashboard/dashboard_analytics.html')

@login_required
def dashboard_sales(request):
    return render(request, 'dashboard/dashboard_sales.html')

@login_required
def dashboard_saas(request):
    return render(request, 'dashboard/dashboard_saas.html')

@login_required
def dashboard_system(request):
    return render(request, 'dashboard/dashboard_system.html')

