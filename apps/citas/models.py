from django.db import models
from apps.especialidades.models import Especialidad
from apps.medicos.models import Medico
from apps.servicios.models import Servicio
from apps.pacientes.models import Paciente


# Create your models here.

class Cita(models.Model):
    paciente = models.ForeignKey('pacientes.Paciente', on_delete=models.CASCADE)
    especialidad = models.ForeignKey('especialidades.Especialidad', on_delete=models.CASCADE)
    medico = models.ForeignKey('medicos.Medico', on_delete=models.CASCADE)
    motivo = models.CharField(max_length=200, null=True,  blank=True)
    servicio = models.ForeignKey('servicios.Servicio', on_delete=models.SET_NULL, null=True)
    fecha = models.DateField()
    hora= models.TimeField()
    duracion = models.CharField(max_length=30, null=True,  blank=True)

    def __str__(self):
        return f"Cita de {self.paciente} con {self.medico} el {self.fecha} a las {self.hora}"