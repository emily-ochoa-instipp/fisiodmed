import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from apps.usuarios.models import Usuario
from apps.medicos.models import Medico
from apps.especialidades.models import Especialidad
from apps.servicios.models import Servicio
from apps.pacientes.models import Paciente
from apps.citas.models import Cita


@pytest.mark.django_db
def test_editar_cita_funciona_correctamente(client):
    user = User.objects.create_user(username="doctor", password="12345")
    usuario = Usuario.objects.create(user=user, rol="Médico")
    client.login(username="doctor", password="12345")

    especialidad = Especialidad.objects.create(nombre="Fisioterapia")
    servicio = Servicio.objects.create(nombre="Terapia física", especialidad=especialidad)
    medico = Medico.objects.create(
        usuario=usuario,
        especialidad=especialidad,
        direccion="Av. Salud 123"
    )

    paciente = Paciente.objects.create(
        usuario=usuario,
        direccion="Calle Paciente 45",
        sexo="F",
        edad=25
    )

    cita = Cita.objects.create(
        paciente=paciente,
        especialidad=especialidad,
        medico=medico,
        servicio=servicio,
        motivo="Chequeo inicial",
        fecha="2025-11-15",
        hora="09:00",
        duracion="30 minutos",
    )

    url = reverse("editar_cita", args=[cita.id])
    response = client.get(url)
    assert response.status_code == 200, "❌ La vista de edición no carga correctamente."
