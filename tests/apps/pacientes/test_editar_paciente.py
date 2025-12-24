import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from apps.usuarios.models import Usuario
from apps.pacientes.models import Paciente


@pytest.mark.django_db
def test_cargar_pagina_editar_paciente(client):
    # Usuario admin para acceder
    admin = User.objects.create_user(
        username="admin",
        password="12345"
    )
    client.login(username="admin", password="12345")

    # Crear User base
    u = User.objects.create_user(
        username="pac1",
        password="pass123",
        first_name="Carlos",
        last_name="Lopez",
        email="carlos@example.com"
    )

    # Usuario extendido
    usuario_ext = Usuario.objects.create(
        user=u,
        num_doc="1234567890",
        telefono="0991122334"
    )

    # Crear paciente con todos los datos usados en tu template
    paciente = Paciente.objects.create(
        usuario=usuario_ext,
        fecha_nac="2000-05-10",
        edad=24,
        sexo="Masculino",
        tipo_sangre="A+",
        direccion="Av. Siempre Viva",
        estado_civil="Solter@"
    )

    url = reverse("editar_paciente", args=[paciente.id])
    resp = client.get(url)

    assert resp.status_code == 200

    html = resp.content.decode()

    # --- Validar presencia de todos los campos importantes en el template ---
    assert "Carlos" in html
    assert "Lopez" in html
    assert "2000-05-10" in html
    assert "24" in html
    assert "Masculino" in html
    assert "A+" in html
    assert "1234567890" in html
    assert "0991122334" in html
    assert "carlos@example.com" in html
    assert "Av. Siempre Viva" in html
    assert "Solter@" in html
