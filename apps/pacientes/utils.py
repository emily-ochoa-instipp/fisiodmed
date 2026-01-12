from django.shortcuts import get_object_or_404
from apps.pacientes.models import Paciente

def get_paciente_segun_usuario(user, paciente_id):
    # ADMIN y RECEPCIONISTA
    if user.groups.filter(name__in=['Administrador', 'Recepcionista']).exists():
        return get_object_or_404(Paciente, id=paciente_id)

    # MÉDICO ve SOLO SUS PACIENTES
    if user.groups.filter(name='Medico').exists():
        return get_object_or_404(
            Paciente,
            id=paciente_id,
            cita__medico=user.medico
        )

    return None
