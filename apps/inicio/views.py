from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import date
from apps.usuarios.decorators import roles_permitidos

# Create your views here.

@login_required
@user_passes_test(roles_permitidos(['Administrador']))
def index(request):
    return render(request, 'inicio/index.html')

