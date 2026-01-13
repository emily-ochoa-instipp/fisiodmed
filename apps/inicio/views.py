from django.shortcuts import render, redirect
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

    es_medico = user.groups.filter(name='Medico').exists()
    medico = None

    if es_medico:
        medico = Medico.objects.filter(usuario__user=user).first()

    if es_medico and not medico:
        from django.contrib.auth import logout
        logout(request)
        return redirect('login')

    # CITAS
    if es_medico and medico:
        citas_pendientes = Cita.objects.filter(
            estado_cita='pendiente',
            medico=medico
        )
    else:
        citas_pendientes = Cita.objects.filter(estado_cita='pendiente')

    citas_pendientes_count = citas_pendientes.count()

    # PACIENTES
    if es_medico and medico:
        pacientes = Paciente.objects.filter(
            cita__medico=medico
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
