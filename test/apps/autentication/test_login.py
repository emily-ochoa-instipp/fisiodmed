import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_login_template_loads(client):
    """
    Prueba unitaria: verifica que la vista de login responde
    correctamente y carga la plantilla esperada.
    """
    url = reverse('login')
    response = client.get(url)

    assert response.status_code == 200

    html = response.content.decode()
    assert 'fisiomed_login.css' in html
    assert '<h1 class="h5 mb-1">INICIO DE SESIÓN</h1>' in html


@pytest.mark.django_db
def test_login_form_post_invalid(client):
    """
    Prueba unitaria: verifica que el formulario de login devuelve error
    al enviar credenciales incorrectas.
    """
    url = reverse('login')
    response = client.post(url, {
        'username': 'usuario_invalido',
        'password': 'contraseña_incorrecta'
    })

    assert response.status_code == 200

    html = response.content.decode()
    assert 'alert' in html or 'error' in html.lower()
