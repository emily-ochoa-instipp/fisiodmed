import pytest
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User

@pytest.mark.django_db
class TablaPagosViewTests(TestCase):

    def setUp(self):
        # Crear usuario para acceder a la vista protegida
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client.login(username="testuser", password="12345")

    def test_url_tabla_pagos_carga(self):
        url = reverse('tabla_pagos')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_usa_template_correcto(self):
        url = reverse('tabla_pagos')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'pagos/tabla_pagos.html')

    def test_renderiza_componentes_basicos(self):
        url = reverse('tabla_pagos')
        response = self.client.get(url)
        contenido = response.content.decode()

        elementos_presentes = [
            "Listado de pagos",
            "Buscar",
            "Agregar +",
            "Acción",
            "dataTable-1",
            "<th>Fecha</th>",
            "<th>Medio</th>",
            "<th>Monto total</th>",
            "<th>Monto pendiente</th>",
            "<th>Estado</th>",
        ]

        for elem in elementos_presentes:
            assert elem in contenido, f"No se encontró el elemento: {elem}"
