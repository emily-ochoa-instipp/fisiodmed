from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class LoginIntegrationTest(TestCase):

    def setUp(self):
        # Crear un usuario real para probar la integración completa
        self.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )

    def test_login_integration(self):
        """
        Prueba de integración:
        - Carga la página de login
        - Envía los datos del formulario
        - Autentica al usuario
        - Redirige correctamente
        """

        # 1️⃣ Obtener la URL del login
        url = reverse('login')

        # 2️⃣ Enviar petición POST con datos correctos
        response = self.client.post(url, {
            'username': 'testuser',
            'password': '12345',
        })

        # 3️⃣ Debe redirigir al home/dashboard
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
