import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from apps.usuarios.models import Usuario
from apps.medicos.models import Medico
from apps.especialidades.models import Especialidad


@pytest.mark.django_db
def test_cargar_pagina_editar_medico(client):
    # Crear usuario administrador para poder ingresar al sistema
    admin = User.objects.create_user(
        username="admin",
        password="12345"
    )
    client.login(username="admin", password="12345")

    # Crear especialidad
    esp = Especialidad.objects.create(nombre="Fisioterapia")

    # Crear usuario del médico
    u = User.objects.create_user(
        username="doctor1",
        password="pass123",
        first_name="Mario",
        last_name="Vera",
        email="mario@example.com"
    )

    usuario_ext = Usuario.objects.create(
        user=u,
        num_doc="1112223334",
        telefono="0987654321",
    )

    # Crear médico asociado
    medico = Medico.objects.create(
        usuario=usuario_ext,
        especialidad=esp,
        direccion="Calle A"
    )

    # URL hacia la vista de edición
    url = reverse("editar_medico", args=[medico.id])
    resp = client.get(url)

    assert resp.status_code == 200

    html = resp.content.decode()

    # Validar que los datos aparecen en la vista
    assert "Mario" in html
    assert "Vera" in html
    assert "Fisioterapia" in html
    assert "1112223334" in html
    assert "0987654321" in html
    assert "mario@example.com" in html
    assert "Calle A" in html
