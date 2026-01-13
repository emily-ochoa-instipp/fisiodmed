from apps.medicos.models import Medico
from apps.pacientes.models import Paciente

def get_paciente_segun_usuario(user, paciente_id):

    # ADMIN y RECEPCIONISTA → acceso total
    if user.groups.filter(name__in=['Administrador', 'Recepcionista']).exists():
        return Paciente.objects.filter(id=paciente_id).first()

    # MÉDICO → solo sus pacientes
    if user.groups.filter(name='Medico').exists():
        try:
            medico = Medico.objects.get(usuario=user.usuario)
        except Medico.DoesNotExist:
            return None

        return Paciente.objects.filter(
            id=paciente_id,
            cita__medico=medico
        ).distinct().first()

    return None
