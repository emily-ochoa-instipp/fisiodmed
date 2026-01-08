
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from apps.citas.models import Cita
from apps.medicos.models import Medico
from apps.servicios.models import Servicio
from apps.pacientes.models import Paciente
from apps.pagos.models import Pago
from datetime import datetime, date
from apps.usuarios.decorators import roles_permitidos
from django.contrib import messages
from django.http import JsonResponse
from decimal import Decimal

# Create your views here.

@login_required
@user_passes_test(roles_permitidos(['Secretaria', 'Medico','Administrador', 'Recepcionista']))
def calendar(request):
    return render(request, 'citas/calendar.html', {
        'pacientes': Paciente.objects.all(),
        'medicos': Medico.objects.all(),
        'servicios': Servicio.objects.all(),
    })


@login_required
@user_passes_test(roles_permitidos(['Secretaria', 'Medico','Administrador', 'Recepcionista']))
def tabla_citas(request):
    citas = Cita.objects.all()
    pacientes = Paciente.objects.all()
    medicos = Medico.objects.all()
    servicios = Servicio.objects.all()

    return render(request, 'citas/tabla_citas.html', {
        'citas': citas,
        'pacientes': pacientes,
        'medicos': medicos,
        'servicios': servicios,
    })

@login_required
@user_passes_test(roles_permitidos(['Administrador', 'Recepcionista']))
def registrar_cita(request):
    if request.method != 'POST':
        return redirect('tabla_citas')

    try:
        fecha_str = request.POST.get('txtFecha')
        hora_str = request.POST.get('txtHora')

        if not fecha_str or not hora_str:
            messages.error(request, 'Fecha y hora son obligatorias.')
            return redirect('tabla_citas')

        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        hora = datetime.strptime(hora_str, '%H:%M').time()

        if fecha < date.today():
            messages.error(request, 'No se puede registrar una cita en una fecha pasada.')
            return redirect('tabla_citas')

        paciente_id = request.POST.get('txtPaciente')
        medico_id = request.POST.get('txtMedico')
        servicio_id = request.POST.get('txtServicio')

        motivo = request.POST.get('txtMotivo', '').strip()
        duracion = request.POST.get('txtDuracion', '').strip()

        # VALIDAR FK 
        paciente = Paciente.objects.get(id=paciente_id)
        medico = Medico.objects.get(id=medico_id)
        servicio = Servicio.objects.get(id=servicio_id)

        #  VALIDACIÓN DE CHOQUE 
        existe = Cita.objects.filter(medico=medico,fecha=fecha,hora=hora).exists()

        if existe:
            messages.error(request,'El médico ya tiene una cita registrada en esa fecha y hora.')
            return redirect('tabla_citas')

        cita = Cita.objects.create(
            paciente=paciente,
            medico=medico,
            servicio=servicio,
            motivo=motivo,
            fecha=fecha,
            hora=hora,
            duracion=duracion,
        )

        # PAGO OPCIONAL
        monto = request.POST.get('monto')
        metodo = request.POST.get('metodo')

        if monto:
            monto = Decimal(monto)

            if monto > 0 and monto <= cita.total_servicio():
                Pago.objects.create(
                    cita=cita,
                    monto=monto,
                    metodo=metodo
                )
                cita.actualizar_estado_pago()

        messages.success(request, 'Cita registrada correctamente.')
        return redirect('tabla_citas')

    except Paciente.DoesNotExist:messages.error(request, 'Paciente no válido.')
    except Medico.DoesNotExist:messages.error(request, 'Médico no válido.')
    except Servicio.DoesNotExist:messages.error(request, 'Servicio no válido.')
    except ValueError:messages.error(request, 'Formato de fecha u hora incorrecto.')
    except Exception:messages.error(request, 'Ocurrió un error inesperado al registrar la cita.')

    return redirect('tabla_citas')

@login_required
@user_passes_test(roles_permitidos(['Administrador', 'Recepcionista']))
def editar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)

    if request.method == 'POST':
        try:
            cita.paciente_id = request.POST.get('txtPaciente')
            cita.medico_id = request.POST.get('txtMedico')
            cita.servicio_id = request.POST.get('txtServicio')
            cita.motivo = request.POST.get('txtMotivo')
            cita.duracion = request.POST.get('txtDuracion')

            cita.fecha = datetime.strptime(request.POST.get('txtFecha'), '%Y-%m-%d').date()

            cita.hora = datetime.strptime(request.POST.get('txtHora'), '%H:%M').time()

            existe = Cita.objects.filter(
                medico_id=cita.medico_id,
                fecha=cita.fecha,
                hora=cita.hora
            ).exclude(id=cita.id).exists()

            if existe:
                messages.error(request, 'El médico ya tiene otra cita en ese horario.')
                return redirect('editar_cita', cita_id=cita.id)

            cita.save()
            messages.success(request, 'Cita actualizada correctamente.')
            return redirect('tabla_citas')

        except Exception:
            messages.error(request, 'Error al actualizar la cita.')

    return render(request, 'citas/editar_cita.html', {
        'cita': cita,
        'pacientes': Paciente.objects.all(),
        'medicos': Medico.objects.all(),
        'servicios': Servicio.objects.all(),
        'pagos': cita.pagos.all(),
        'METODOS_PAGO': Pago.METODO_PAGO,
    })


@login_required
@user_passes_test(roles_permitidos(['Administrador', 'Recepcionista']))

def eliminar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    cita.delete()
    return redirect('tabla_citas')

@login_required
@user_passes_test(roles_permitidos(['Administrador', 'Recepcionista']))
def citas_calendario(request):
    citas = Cita.objects.all()
    eventos = []

    for cita in citas:
        eventos.append({
            'title': f'{cita.paciente}',
            'start': f'{cita.fecha}T{cita.hora}',
            # Datos adicionales para el tooltip
            'extendedProps': {
                'medico': str(cita.medico),
                'motivo': cita.motivo,
                'servicio': str(cita.servicio),
                'hora': cita.hora.strftime("%H:%M")
            }
        })

    return JsonResponse(eventos, safe=False)

