import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from apps.especialidades.models import Especialidad


@pytest.mark.django_db
def test_cargar_pagina_editar_especialidad(client):

    # Crear usuario y loguear
    user = User.objects.create_user(username="admin", password="12345")
    client.login(username="admin", password="12345")

    esp = Especialidad.objects.create(nombre="Fisioterapia")

    url = reverse('editar_especialidad', args=[esp.id])
    resp = client.get(url)

    assert resp.status_code == 200
    assert "Fisioterapia" in resp.content.decode()
