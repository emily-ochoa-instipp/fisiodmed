from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date

# Create your views here.

@login_required
def index(request):
    return render(request, 'inicio/index.html')

