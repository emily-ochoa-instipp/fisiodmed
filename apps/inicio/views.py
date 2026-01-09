from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import date

from apps.citas.models import Cita
from apps.pacientes.models import Paciente
from apps.usuarios.models import Usuario
from apps.medicos.models import Medico
from apps.usuarios.decorators import roles_permitidos


@login_required
@user_passes_test(roles_permitidos(['Secretaria', 'Presidenta','Administrador']))

def inicio(request):
    hoy = date.today()

    # CITAS
    citas_pendientes = Cita.objects.filter(estado_cita='pendiente')
    citas_pendientes_count = citas_pendientes.count()

    # PACIENTES
    pacientes = Paciente.objects.filter()
    pacientes_count = pacientes.count()

    #MEDICOS
    medicos_activos = Medico.objects.filter()
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

