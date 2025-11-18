# tests/e2e/test_admin_creates_user_e2e.py
from django.urls import reverse
from django.contrib.auth.models import User
import pytest

pytestmark = pytest.mark.e2e
pytestmark = pytest.mark.django_db(transaction=True)


@pytest.mark.django_db
def test_admin_crea_usuario_por_ui(live_server, page):

    # Crear superusuario admin
    admin_username = "admin"
    admin_password = "admin123"

    User.objects.create_superuser(
        username=admin_username,
        email="admin@example.com",
        password=admin_password
    )

    # Datos del nuevo usuario (adaptados a TU formulario real)
    nuevo = {
        "txtUsername": "nuevo_user",
        "txtEmail": "nuevo@example.com",
        "txtNombres": "NUEVO",
        "txtApellidos": "USUARIO",
        "txtPassword": "password123",
        "txtNumDoc": "0955555555",
        "txtTelefono": "0999999999",
    }

    # 1) LOGIN UI
    login_url = live_server.url + reverse("login")
    page.goto(login_url)

    page.fill("input[name='username']", admin_username)
    page.fill("input[name='password']", admin_password)

    page.click("button[type='submit']")   # ← tu login tiene button, no input

    # 2) IR A LA PÁGINA Y ABRIR EL MODAL
    add_user_url = live_server.url + reverse("tabla-usuarios")
    page.goto(add_user_url)

    # Abrir modal Agregar usuario
    page.click('button[data-target="#eventModal"]')
    page.wait_for_selector('#eventModal', state="visible")

    # 3) LLENAR CAMPOS REALES
    page.select_option('select[name="txtRol"]', "Paciente")
    page.fill('input[name="txtNombres"]', nuevo["txtNombres"])
    page.fill('input[name="txtApellidos"]', nuevo["txtApellidos"])
    page.fill('input[name="txtEmail"]', nuevo["txtEmail"])
    page.fill('input[name="txtTelefono"]', nuevo["txtTelefono"])
    page.fill('input[name="txtNumDoc"]', nuevo["txtNumDoc"])
    page.fill('input[name="txtUsername"]', nuevo["txtUsername"])
    page.fill('input[name="txtPassword"]', nuevo["txtPassword"])

    # 4) GUARDAR
    page.click("button[type='submit']")

    # 5) VALIDACIÓN DB
    assert User.objects.filter(username=nuevo["txtUsername"]).exists()
