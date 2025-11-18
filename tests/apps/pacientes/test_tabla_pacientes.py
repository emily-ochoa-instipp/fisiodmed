import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from apps.usuarios.models import Usuario
from apps.pacientes.models import Paciente

@pytest.mark.django_db
def test_tabla_pacientes_muestra_lista(client):
    # Crear usuario base
    user = User.objects.create_user(
        username="usuario1",
        first_name="Juan",
        last_name="Pérez",
        email="juan@example.com"
    )

    usuario = Usuario.objects.create(
        user=user,
        num_doc="1234567890",
        telefono="0999999999"
    )

    # Crear un paciente ligado al usuario
    Paciente.objects.create(
        usuario=usuario,
        edad=30,
        sexo="Masculino",
        direccion="Av. Siempre Viva 123"
    )

    client.force_login(user)  # 👈 NECESARIO

    url = reverse("tabla_pacientes")
    response = client.get(url)

    assert response.status_code == 200
    assert b"Pacientes" in response.content or b"Listado" in response.content
