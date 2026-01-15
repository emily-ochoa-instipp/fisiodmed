
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

    user = request.user

    if user.groups.filter(name='Medico').exists():
        usuario = getattr(user, 'usuario', None)
        medico = Medico.objects.filter(usuario=usuario).first() if usuario else None

        medicos = Medico.objects.filter(id=medico.id) if medico else Medico.objects.none()
        pacientes = Paciente.objects.filter(cita__medico=medico).distinct() if medico else Paciente.objects.none()
    else:
        medicos = Medico.objects.all()
        pacientes = Paciente.objects.all()

    return render(request, 'citas/calendar.html', {
        'pacientes': pacientes,
        'medicos': medicos,
        'servicios': Servicio.objects.all(),
    })


@login_required
@user_passes_test(roles_permitidos(['Secretaria', 'Medico','Administrador', 'Recepcionista']))
def tabla_citas(request):

    user = request.user

    if user.groups.filter(name='Medico').exists():
        usuario = getattr(user, 'usuario', None)
        medico = Medico.objects.filter(usuario=usuario).first() if usuario else None
        citas = Cita.objects.filter(medico=medico) if medico else Cita.objects.none()
    else:
        citas = Cita.objects.all()

    return render(request, 'citas/tabla_citas.html', {
        'citas': citas,
        'pacientes': Paciente.objects.all(),
        'medicos': Medico.objects.all(),
        'servicios': Servicio.objects.all(),
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

# Función de validación de transiciones
def estado_valido(estado_actual, nuevo_estado):
    TRANSICIONES_VALIDAS = {
        'pendiente': ['pendiente', 'atendida', 'cancelada', 'no_asistio'],
        'atendida': [],
        'cancelada': [],
        'no_asistio': [],
    }
    return nuevo_estado in TRANSICIONES_VALIDAS.get(estado_actual, [])

@login_required
@user_passes_test(roles_permitidos(['Administrador', 'Recepcionista']))
def editar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)

    # no permitir editar citas finalizadas
    if cita.estado_cita in ['cancelada', 'no_asistio']:
        messages.error(request,'No se puede modificar una cita que fue cancelada o no asistida.')
        return redirect('tabla_citas')

    if request.method == 'POST':
        try:
            nuevo_estado = request.POST.get('estado')

            # Validar que el estado exista
            if nuevo_estado not in dict(Cita.ESTADOS_CITA):
                messages.error(request, 'Estado de cita no válido.')
                return redirect('editar_cita', cita.id)

            # No permitir cambios si el estado es final
            if not estado_valido(cita.estado_cita, nuevo_estado):
                messages.error(request,'No se puede cambiar el estado de la cita.')
                return redirect('editar_cita', cita.id)

            cita.paciente_id = request.POST.get('txtPaciente')
            cita.medico_id = request.POST.get('txtMedico')
            cita.servicio_id = request.POST.get('txtServicio')
            cita.duracion = request.POST.get('txtDuracion')

            cita.fecha = datetime.strptime(request.POST.get('txtFecha'), '%Y-%m-%d').date()

            cita.hora = datetime.strptime(request.POST.get('txtHora'), '%H:%M').time()

            #  Validar choque de horario
            existe = Cita.objects.filter(
                medico_id=cita.medico_id,
                fecha=cita.fecha,
                hora=cita.hora
            ).exclude(id=cita.id).exists()

            if existe:
                messages.error(request, 'El médico ya tiene otra cita en ese horario.')
                return redirect('editar_cita', cita_id=cita.id)

            cita.estado_cita = nuevo_estado
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
        'ESTADOS_CITA': Cita.ESTADOS_CITA,
    })


@login_required
@user_passes_test(roles_permitidos(['Administrador', 'Recepcionista']))

def eliminar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    cita.delete()
    return redirect('tabla_citas')


@login_required
@user_passes_test(roles_permitidos(['Administrador', 'Recepcionista', 'Medico']))
def citas_calendario(request):

    user = request.user  # usuario logueado

    # ADMIN  y RECEPCIONISTA VEN TODAS LAS CITAS
    if user.is_superuser or user.groups.filter(
        name__in=['Administrador', 'Recepcionista']
    ).exists():
        citas = Cita.objects.all()

    # 2MÉDICO  SOLO  VE SUS CITAS
    elif user.groups.filter(name='Medico').exists():
        usuario = getattr(user, 'usuario', None)

        if usuario:
            medico = Medico.objects.filter(usuario=usuario).first()
            citas = Cita.objects.filter(medico=medico) if medico else Cita.objects.none()
        else:
            citas = Cita.objects.none()

    # OTROS  NADA
    else:
        citas = Cita.objects.none()

    eventos = []

    for cita in citas:
        # COLORES SEGÚN ESTADO DE LA CITA
        colores = {
            'pendiente': "#eea303",
            'atendida': "#28a76e",
            'cancelada': '#dc3545',
            'no_asistio': '#6c757d',
        }

        eventos.append({
            'title': str(cita.paciente),
            'start': f'{cita.fecha}T{cita.hora}',
            'backgroundColor': colores.get(cita.estado_cita),
            'borderColor': colores.get(cita.estado_cita),
            # Datos  para el tooltip
            'extendedProps': {
                'medico': str(cita.medico),
                'servicio': str(cita.servicio),
                'hora': cita.hora.strftime('%H:%M'),
                'estado_cita': cita.get_estado_cita_display(),
                'estado_pago': cita.get_estado_pago_display(),
            }
        })

    return JsonResponse(eventos, safe=False)
