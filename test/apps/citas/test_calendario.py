import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from apps.usuarios.models import Usuario
from apps.citas.models import Cita
from apps.pacientes.models import Paciente
from apps.medicos.models import Medico
from apps.especialidades.models import Especialidad
from apps.servicios.models import Servicio


@pytest.mark.django_db
def test_vista_calendario_citas_renderiza_correctamente(client):
    """
    ✅ Prueba que la vista del calendario de citas se carga correctamente.
    """
    user = User.objects.create_user(username="doctor", password="12345")
    usuario = Usuario.objects.create(user=user, rol="Médico")
    client.login(username="doctor", password="12345")

    especialidad = Especialidad.objects.create(nombre="Fisioterapia")
    servicio = Servicio.objects.create(nombre="Terapia física", especialidad=especialidad)
    medico = Medico.objects.create(
        usuario=usuario,
        especialidad=especialidad,
        direccion="Av. Siempre Viva 123"
    )

    paciente = Paciente.objects.create(
        usuario=usuario,
        direccion="Calle Salud 101",
        sexo="M",
        edad=30
    )

    Cita.objects.create(
        paciente=paciente,
        especialidad=especialidad,
        medico=medico,
        servicio=servicio,
        motivo="Dolor de espalda",
        fecha="2025-11-11",
        hora="10:00",
        duracion="30 minutos",
    )

    url = reverse("calendar")
    response = client.get(url)

    assert response.status_code == 200, "❌ La vista no responde con código 200."
    html = response.content.decode()
    assert "calendario" in html.lower() or "citas" in html.lower(), "❌ El template del calendario no se muestra correctamente."


@pytest.mark.django_db
def test_calendario_requiere_autenticacion(client):
    """
    ✅ Prueba que el calendario redirige si el usuario no está autenticado.
    """
    url = reverse("calendar")
    response = client.get(url)
    assert response.status_code in [302, 401], "❌ La vista debería requerir autenticación."
