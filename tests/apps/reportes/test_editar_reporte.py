import pytest
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User


@pytest.mark.django_db
class EditarReporteViewTests(TestCase):

    def setUp(self):
        # Usuario para pasar el login_required
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client.login(username="testuser", password="12345")

    def test_url_editar_reporte_carga(self):
        url = reverse('editar_reporte')  # Ajusta el nombre si es diferente
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_usa_template_correcto(self):
        url = reverse('editar_reporte')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'reportes/editar_reporte.html')

    def test_renderiza_componentes_basicos(self):
        url = reverse('editar_reporte')
        response = self.client.get(url)
        contenido = response.content.decode()

        elementos = [
            "Editar reporte",
            "Nombres",
            "Apellidos",
            "Fecha de nacimiento",
            "Edad",
            "Sexo",
            "Tipo de sangre",
            "Tipo documento",
            "Número documento",
            "Número teléfono",
            "Email",
            "Dirección",
            "Estado civil",
            "Guardar",
            "Cancelar",
            "inputNombres",
            "inputApellidos",
            "inputFchNac",
            "inputEdad",
            "inputSexo",
            "inputTipoSangre",
            "inputTipoDoc",
            "inputNumDoc",
            "inputNumTelf",
            "inputEmail",
            "inputDireccion",
            "inputEstadoCivil",
        ]

        for elem in elementos:
            assert elem in contenido, f"No se encontró el elemento: {elem}"
