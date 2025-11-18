import pytest
from django.urls import reverse
from django.contrib.auth.models import User

pytestmark = [pytest.mark.django_db(transaction=True)]

def test_admin_crea_usuario_por_ui(live_server, page):

    # ========================
    # CREAR ADMIN
    # ========================
    admin_pass = "anahi$1234"
    admin = User.objects.create_superuser(
        username="anahi1234",
        email="anahi@example.com",
        password=admin_pass,
    )

    # DATOS DEL USUARIO NUEVO SEGÚN TU FORMULARIO HTML
    nuevo = {
        "txtNombres": "Nuevo",
        "txtApellidos": "Usuario",
        "txtUsername": "nuevo_user",
        "txtPassword": "clave1234",
        "txtEmail": "nuevo@example.com",
        "txtTelefono": "0987654321",
        "txtNumDoc": "1100110011",
    }

    # ========================
    # LOGIN
    # ========================
    login_url = live_server.url + reverse("login")
    page.goto(login_url)

    page.fill('input[name="username"]', admin.username)
    page.fill('input[name="password"]', admin_pass)
    page.click('button[type="submit"]')

    page.wait_for_load_state("networkidle")

    # ========================
    # IR A LISTA DE USUARIOS
    # ========================
    lista_url = live_server.url + reverse("tabla_usuarios")
    page.goto(lista_url)
    page.wait_for_load_state("networkidle")

    # ========================
    # ABRIR MODAL "AGREGAR USUARIO"
    # ========================
    page.click('button[data-target="#eventModal"]')

    # ========================
    # LLENAR FORMULARIO
    # ========================

    # SELECT del rol
    page.select_option('select[name="txtRol"]', label="Recepcionista")  

    # Inputs normales
    for campo, valor in nuevo.items():
        selector = f'input[name="{campo}"]'
        page.fill(selector, valor)

    # ========================
    # GUARDAR
    # ========================
    page.click('button[type="submit"]')
    page.wait_for_load_state("networkidle")

    # ========================
    # VALIDAR BD
    # ========================
    assert User.objects.filter(username=nuevo["txtUsername"]).exists(), (
        " El usuario no se creó en la base de datos"
    )
