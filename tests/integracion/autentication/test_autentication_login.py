import pytest
from django.urls import reverse
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_login_page_loads(client):
    """La página de login debe cargar correctamente."""
    url = reverse('login')
    response = client.get(url)

    assert response.status_code == 200
    assert b"INICIO DE SES" in response.content   # evita problemas de tildes
    assert b"USUARIO" in response.content
    assert b"CONTRASE" in response.content        # evita problemas con ñ y tilde


@pytest.mark.django_db
def test_login_success(client):
    """Debe permitir iniciar sesión con credenciales correctas."""
    User.objects.create_user(username="testuser", password="12345")

    url = reverse('login')
    response = client.post(url, {
        "username": "testuser",
        "password": "12345",
    }, follow=True)

    # Tu vista NO redirige, por eso se espera 200
    assert response.status_code == 200

    # Verifica que el usuario inició sesión revisando el contexto
    assert response.wsgi_request.user.is_authenticated is True


@pytest.mark.django_db
def test_login_fail(client):
    """Debe mostrar error si las credenciales son incorrectas."""
    url = reverse('login')
    response = client.post(url, {
        "username": "fakeuser",
        "password": "wrongpass",
    })

    # Debe volver a cargar la misma página
    assert response.status_code == 200

    # Mensaje de error presente
    assert b"alert-danger" in response.content
