import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from apps.pacientes.models import Paciente, Usuario

@pytest.mark.django_db
def test_get_editar_paciente(client):
    # Crear usuario del sistema
    user = User.objects.create_user(
        username="testuser",
        password="12345",
        first_name="Juan",
        last_name="Pérez",
    )

    # Crear objeto Usuario (tu modelo intermedio)
    usuario = Usuario.objects.create(
        user=user,
        num_doc="1234567890",
        telefono="0999999999",
    )

    # Crear paciente
    paciente = Paciente.objects.create(
        usuario=usuario,
        fecha_nac="2000-01-01",
        edad=24,
        sexo="Masculino",
        tipo_sangre="O+",
        direccion="Av Siempre Viva",
        estado_civil="Solter@",
    )

    # Login
    client.login(username="testuser", password="12345")

    # URL
    url = reverse("editar_paciente", args=[paciente.id])

    # GET
    response = client.get(url)

    assert response.status_code == 200
    assert b"Editar registro m\xc3\xa9dico" in response.content
    assert b"Nombres" in response.content
    assert b"Apellidos" in response.content
    assert b"Fecha de nacimiento" in response.content


@pytest.mark.django_db
def test_post_editar_paciente(client):
    # Crear usuario y paciente
    user = User.objects.create_user(
        username="testuser",
        password="12345",
        first_name="Juan",
        last_name="Pérez",
    )

    usuario = Usuario.objects.create(
        user=user,
        num_doc="1234567890",
        telefono="0999999999",
    )

    paciente = Paciente.objects.create(
        usuario=usuario,
        fecha_nac="2000-01-01",
        edad=24,
        sexo="Masculino",
        tipo_sangre="O+",
        direccion="Av Siempre Viva",
        estado_civil="Solter@",
    )

    # Login
    client.login(username="testuser", password="12345")

    url = reverse("editar_paciente", args=[paciente.id])

    # POST
    response = client.post(url, {
        "txtNombres": "Carlos",
        "txtApellidos": "Ramírez",
        "txtFechNacimiento": "1999-05-05",
        "txtEdad": "25",
        "txtSexo": "Masculino",
        "txtTipoSangre": "A+",
        "txtNumDoc": "1112223334",
        "txtTelefono": "0888888888",
        "txtEmail": "nuevo@example.com",
        "txtDireccion": "Nueva dirección",
        "txtEstadoCivil": "Casad@"
    })

    # Debe redirigir a la tabla
    assert response.status_code == 302

    # Refrescar cambios
    paciente.refresh_from_db()
    usuario.refresh_from_db()
    usuario.user.refresh_from_db()

    assert usuario.user.first_name == "Carlos"
    assert usuario.user.last_name == "Ramírez"
    assert paciente.tipo_sangre == "A+"
    assert paciente.estado_civil == "Casad@"
