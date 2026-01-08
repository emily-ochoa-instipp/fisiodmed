from django.db import models
from apps.medicos.models import Medico
from apps.servicios.models import Servicio
from apps.pacientes.models import Paciente
from django.db.models import Sum
from decimal import Decimal

# Create your models here.

class Cita(models.Model):
    paciente = models.ForeignKey('pacientes.Paciente', on_delete=models.CASCADE)
    servicio = models.ForeignKey('servicios.Servicio', on_delete=models.SET_NULL, null=True)
    medico = models.ForeignKey('medicos.Medico', on_delete=models.CASCADE)

    fecha = models.DateField()
    hora= models.TimeField()
    duracion = models.CharField(max_length=40, null=True,  blank=True)
    estado_cita = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('atendida', 'Atendida'), ('cancelada', 'Cancelada')],default='pendiente')
    estado_pago = models.CharField(max_length=10,choices=[('pendiente', 'Pendiente'),('parcial', 'Parcial'),('pagado', 'Pagado'),],default='pendiente')

    def __str__(self):
        return f"Cita de {self.paciente} con {self.medico} el {self.fecha} a las {self.hora}"

# LÓGICA DE PAGOS 

    def total_servicio(self):
        return self.servicio.costo if self.servicio else Decimal('0.00')

    def total_pagado(self):
        return self.pagos.aggregate(total=Sum('monto'))['total'] or Decimal('0.00')

    def saldo_pendiente(self):
        return self.total_servicio() - self.total_pagado()

    def actualizar_estado_pago(self):
        if self.total_pagado() == 0:
            self.estado_pago = 'pendiente'
        elif self.total_pagado() < self.total_servicio():
            self.estado_pago = 'parcial'
        else:
            self.estado_pago = 'pagado'

        self.save(update_fields=['estado_pago'])