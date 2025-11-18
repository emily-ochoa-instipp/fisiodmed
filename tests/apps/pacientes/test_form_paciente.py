from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class FormPacientesViewTests(TestCase):

    def setUp(self):
        # Crear usuario para saltar el login_required
        self.user = User.objects.create_user(
            username='testuser',
            password='pass1234'
        )
        self.client.force_login(self.user)

    def test_url_form_pacientes_carga(self):
        url = reverse('form_pacientes')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_usa_template_correcto(self):
        url = reverse('form_pacientes')
        response = self.client.get(url)

        # NOMBRE CORRECTO DEL TEMPLATE
        self.assertTemplateUsed(response, 'pacientes/form_pacientes.html')

    def test_renderiza_campos_principales(self):
        url = reverse('form_pacientes')
        response = self.client.get(url)

        campos = [
            'Nombres', 'Apellidos', 'Fecha de nacimiento',
            'Edad', 'Sexo', 'Dirección', 'Guardar'
        ]

        for campo in campos:
            self.assertContains(response, campo)
