from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from apps.pagos.models import Pago

# Create your views here.

@login_required
def tabla_pagos(request):
    return render(request, 'pagos/tabla_pagos.html')

@login_required
def editar_pago(request, id):
    pago = get_object_or_404(Pago, id=id)
    return render(request, 'pagos/editar_pago.html', {"pago": pago})
