import pytest
from django.urls import reverse
from django.test import TestCase
from apps.pagos.models import Pago
from datetime import date
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class EditarPagoViewTests(TestCase):

    def setUp(self):
        # Usuario para saltar login_required
        self.user = User.objects.create_user(
            username="testuser", password="pass1234"
        )
        self.client.force_login(self.user)

        # Crear pago de prueba
        self.pago = Pago.objects.create(
            fecha=date(2024, 1, 1),
            medio="Efectivo",
            monto_total=50.00,
            monto_pendiente=10.00,
            estado="Pago parcial",
        )

    def test_url_editar_pago_carga(self):
        url = reverse('editar_pago', args=[self.pago.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_usa_template_correcto(self):
        url = reverse('editar_pago', args=[self.pago.id])
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'pagos/editar_pago.html')

    def test_renderiza_campos_principales(self):
        url = reverse('editar_pago', args=[self.pago.id])
        response = self.client.get(url)
        contenido = response.content.decode()

        campos = [
            "inputPaciente",
            "inputFchN",
            "inputServicio",
            "inputMedio",
            "inputMontoT",
            "inputMontoP",
            "inputEstado",
        ]

        for campo in campos:
            assert campo in contenido, f"El campo {campo} no se encontró en el HTML"
