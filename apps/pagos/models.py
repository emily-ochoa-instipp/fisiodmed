from django.db import models
from apps.citas.models import Cita

# Create your models here.


class Pago(models.Model):
    METODO_PAGO = [
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia'),
        ('tarjeta', 'Tarjeta'),
    ]
    
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE, related_name='pagos')
    monto = models.DecimalField(max_digits=8, decimal_places=2)
    metodo = models.CharField(max_length=20,choices=METODO_PAGO, default='efectivo')
    fecha = models.DateTimeField(auto_now_add=True)
    observacion = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Pago ${self.monto} - Cita {self.cita.id}"
