from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def tabla_pagos(request):
    return render(request, 'pagos/tabla_pagos.html')

@login_required
def editar_pago(request):
    return render(request, 'pagos/editar_pago.html')