import pytest
from datetime import date, time
from django.contrib.auth.models import User
from apps.usuarios.models import Usuario
from apps.pacientes.models import Paciente
from apps.especialidades.models import Especialidad
from apps.medicos.models import Medico
from apps.servicios.models import Servicio
from apps.citas.models import Cita

@pytest.mark.django_db
def test_crear_cita():
    # Usuario base para paciente
    user = User.objects.create_user(
        username="juan", password="1234",
        first_name="Juan", last_name="Pérez"
    )
    usuario = Usuario.objects.create(user=user)

    # Paciente
    paciente = Paciente.objects.create(
        usuario=usuario,
        fecha_nac=date(2000, 1, 1),
        edad=25,
        sexo="M",
        tipo_sangre="O+",
        direccion="Av. Siempre Viva",
        estado_civil="Soltero"
    )

    # Especialidad
    especialidad = Especialidad.objects.create(nombre="Fisioterapia")

    # Usuario base para médico
    user_medico = User.objects.create_user(
        username="carlos", password="1234",
        first_name="Carlos", last_name="Ramírez"
    )
    usuario_medico = Usuario.objects.create(user=user_medico)

    # Médico
    medico = Medico.objects.create(
        usuario=usuario_medico,
        especialidad=especialidad,
        direccion="Calle 1"
    )

    # Servicio (CORREGIDO: requiere especialidad)
    servicio = Servicio.objects.create(
        nombre="Terapia Manual",
        especialidad=especialidad     # ← obligatorio
    )

    # Crear la cita
    cita = Cita.objects.create(
        paciente=paciente,
        especialidad=especialidad,
        medico=medico,
        servicio=servicio,
        motivo="Dolor lumbar",
        fecha=date(2025, 1, 1),
        hora=time(9, 30),
        duracion="30 minutos"
    )

    # Validaciones
    assert cita.id is not None
    assert cita.medico == medico
    assert cita.paciente == paciente
    assert cita.servicio == servicio
    assert cita.especialidad == especialidad
