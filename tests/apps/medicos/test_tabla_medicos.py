import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from apps.usuarios.models import Usuario
from apps.medicos.models import Medico
from apps.especialidades.models import Especialidad


@pytest.mark.django_db
def test_tabla_medicos_muestra_lista(client):
    # Crear usuario administrador
    user_admin = User.objects.create_user(
        username="admin",
        password="12345"
    )

    client.login(username="admin", password="12345")

    # Crear especialidad
    esp = Especialidad.objects.create(nombre="Fisioterapia")

    # Crear usuario normal vinculado a Medico
    user1 = User.objects.create_user(
        username="medico1",
        password="pass123",
        first_name="Carlos",
        last_name="Gómez",
        email="carlos@example.com"
    )

    usuario1 = Usuario.objects.create(
        user=user1,
        num_doc="123456",
        telefono="0999999999",
    )

    medico1 = Medico.objects.create(
        usuario=usuario1,
        especialidad=esp,
        direccion="Av. Quito"
    )

    url = reverse("tabla_medicos")
    resp = client.get(url)

    assert resp.status_code == 200
    html = resp.content.decode()

    assert "Carlos" in html
    assert "Gómez" in html
    assert "Fisioterapia" in html
    assert "123456" in html
    assert "0999999999" in html
    assert "carlos@example.com" in html
    assert "Av. Quito" in html
