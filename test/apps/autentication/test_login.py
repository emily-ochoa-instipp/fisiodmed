import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_login_template_loads(client):
    """
    Verifica que la plantilla de inicio de sesión se carga correctamente.
    """
    url = reverse('login')
    response = client.get(url)

    # Verifica que la página carga correctamente
    assert response.status_code == 200

    html = response.content.decode()

    # Verifica que contiene el CSS y el título del login
    assert 'fisiomed_login.css' in html
    assert '<h1 class="h5 mb-1">INICIO DE SESIÓN</h1>' in html


@pytest.mark.django_db
def test_login_form_post_invalid(client):
    """
    Verifica que al enviar credenciales incorrectas se muestre un error.
    """
    url = reverse('login')
    response = client.post(url, {
        'username': 'usuario_invalido',
        'password': 'contraseña_incorrecta'
    })

    # No debe redirigir (debe recargar el mismo formulario)
    assert response.status_code == 200

    html = response.content.decode()

    # Verifica que aparece algún mensaje de error
    assert 'alert' in html or 'error' in html.lower(), "No se encontró mensaje de error en la página"
