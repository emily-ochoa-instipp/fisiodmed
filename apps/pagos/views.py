from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from decimal import Decimal
from django.contrib import messages
from apps.citas.models import Cita
from apps.pagos.models import Pago
from apps.usuarios.decorators import roles_permitidos


# Create your views here.

@login_required
@user_passes_test(roles_permitidos(['Administrador', 'Recepcionista']))

def tabla_pagos(request):
    return render(request, 'pagos/tabla_pagos.html')

@login_required
@user_passes_test(roles_permitidos(['Administrador', 'Recepcionista']))
def registrar_pago(request, cita_id):
    if request.method != 'POST':
        return redirect('editar_cita', cita_id)

    cita = get_object_or_404(Cita, id=cita_id)

    # VALIDACIÓN DE ESTADO DE CITA
    if cita.estado_cita != 'atendida':
        messages.error(
            request,
            'Solo se pueden registrar pagos en citas atendidas.'
        )
        return redirect('editar_cita', cita.id)

    try:
        monto = Decimal(request.POST.get('monto'))
        metodo = request.POST.get('metodo')
        observacion = request.POST.get('observacion')

        if monto <= 0:
            messages.error(request, 'El monto debe ser mayor a cero.')
            return redirect('editar_cita', cita.id)

        if monto > cita.saldo_pendiente():
            messages.error(request, 'El monto supera el saldo pendiente.')
            return redirect('editar_cita', cita.id)

        Pago.objects.create(
            cita=cita,
            monto=monto,
            metodo=metodo,
            observacion=observacion
        )

        cita.actualizar_estado_pago()
        messages.success(request, 'Pago registrado correctamente.')
        return redirect('editar_cita', cita.id)

    except Exception:
        messages.error(request, 'Error al registrar el pago.')
        return redirect('editar_cita', cita.id)


@login_required
@user_passes_test(roles_permitidos(['Administrador', 'Recepcionista']))
def editar_pago(request, pago_id):
    pago = get_object_or_404(Pago, id=pago_id)
    cita = pago.cita

    if cita.estado_cita != 'atendida':
        messages.error(
            request,
            'No se pueden modificar pagos de una cita no atendida.'
        )
        return redirect('editar_cita', cita.id)

    if request.method == 'POST':
        monto = Decimal(request.POST.get('monto'))
        metodo = request.POST.get('metodo')
        observacion = request.POST.get('observacion')

        # Recalcular saldo sin este pago
        total_pagado = sum(p.monto for p in cita.pagos.exclude(id=pago.id))
        saldo = cita.total_servicio() - total_pagado

        if monto > saldo:
            messages.error(request, 'El monto supera el saldo pendiente')
            return redirect('editar_pago', pago.id)

        pago.monto = monto
        pago.metodo = metodo
        pago.observacion = observacion
        pago.save()

        cita.actualizar_estado_pago()

        messages.success(request, 'Pago actualizado correctamente')
        return redirect('editar_cita', cita.id)

    return render(request, 'pagos/editar_pago.html', {
        'pago': pago,
        'METODOS_PAGO': Pago.METODO_PAGO
    })

@login_required
@user_passes_test(roles_permitidos(['Administrador', 'Recepcionista']))
def eliminar_pago(request, pago_id):
    pago = get_object_or_404(Pago, id=pago_id)
    cita = pago.cita

    if cita.estado_cita != 'atendida':
        messages.error(
            request,
            'No se pueden eliminar pagos de una cita no atendida.'
        )
        return redirect('editar_cita', cita.id)

    pago.delete()
    cita.actualizar_estado_pago()

    messages.success(request, 'Pago eliminado correctamente')
    return redirect('editar_cita', cita.id)
