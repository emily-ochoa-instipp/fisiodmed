from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import date

from apps.citas.models import Cita
from apps.pacientes.models import Paciente
from apps.usuarios.models import Usuario
from apps.medicos.models import Medico
from apps.usuarios.decorators import roles_permitidos


@login_required
@user_passes_test(roles_permitidos(['Recepcionista', 'Medico', 'Administrador']))
def inicio(request):
    hoy = date.today()
    user = request.user

    # CITAS

    if user.groups.filter(name='Medico').exists():
        medico = Medico.objects.get(usuario__user=user)
        citas_pendientes = Cita.objects.filter(
            estado_cita='pendiente',
            medico=medico
        )
    else:
        citas_pendientes = Cita.objects.filter(estado_cita='pendiente')

    citas_pendientes_count = citas_pendientes.count()

    # PACIENTES
    if user.groups.filter(name='Medico').exists():
        pacientes = Paciente.objects.filter(
            citas__medico=medico
        ).distinct()
    else:
        pacientes = Paciente.objects.all()

    pacientes_count = pacientes.count()

    # MEDICOS
    medicos_activos = Medico.objects.all()
    medicos_activos_count = medicos_activos.count()

    # USUARIOS
    usuarios_activos = Usuario.objects.filter(user__is_active=True)
    usuarios_activos_count = usuarios_activos.count()

    context = {
        'citas_pendientes': citas_pendientes,
        'citas_pendientes_count': citas_pendientes_count,

        'pacientes': pacientes,
        'pacientes_count': pacientes_count,

        'usuarios_activos': usuarios_activos,
        'usuarios_activos_count': usuarios_activos_count,

        'medicos_activos': medicos_activos,
        'medicos_activos_count': medicos_activos_count,
    }

    return render(request, 'inicio/inicio.html', context)
