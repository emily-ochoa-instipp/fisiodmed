import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from apps.usuarios.models import Usuario
from apps.medicos.models import Medico
from apps.pacientes.models import Paciente
from apps.especialidades.models import Especialidad
from apps.servicios.models import Servicio
from apps.citas.models import Cita


@pytest.mark.django_db
def test_tabla_citas_renderiza_correctamente(client):
    user = User.objects.create_user(username="doctor", password="12345")
    usuario = Usuario.objects.create(user=user, rol="Médico")
    client.login(username="doctor", password="12345")

    especialidad = Especialidad.objects.create(nombre="Fisioterapia")
    servicio = Servicio.objects.create(nombre="Terapia", especialidad=especialidad)
    medico = Medico.objects.create(
        usuario=usuario,
        especialidad=especialidad,
        direccion="Av. Principal 100"
    )

    paciente = Paciente.objects.create(
        usuario=usuario,
        direccion="Calle Uno",
        sexo="M",
        edad=28
    )

    Cita.objects.create(
        paciente=paciente,
        especialidad=especialidad,
        medico=medico,
        servicio=servicio,
        motivo="Chequeo general",
        fecha="2025-11-20",
        hora="08:00",
        duracion="30 minutos"
    )

    url = reverse("tabla_citas")
    response = client.get(url)
    assert response.status_code == 200, "❌ La vista de tabla de citas no responde con código 200."
