import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from apps.especialidades.models import Especialidad


@pytest.mark.django_db
def test_tabla_especialidades_muestra_lista(client):

    # Crear usuario y loguear
    user = User.objects.create_user(username="admin", password="12345")
    client.login(username="admin", password="12345")

    # Crear datos reales del modelo
    Especialidad.objects.create(nombre="Fisioterapia")
    Especialidad.objects.create(nombre="Odontología")

    url = reverse('tabla_especialidades')
    resp = client.get(url)

    assert resp.status_code == 200
    assert "Fisioterapia" in resp.content.decode()
    assert "Odontología" in resp.content.decode()
