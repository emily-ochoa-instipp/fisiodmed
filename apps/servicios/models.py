from django.db import models

# Create your models here.

class Servicio(models.Model):
    nombre = models.CharField(max_length=255)
    especialidad = models.ForeignKey('especialidades.Especialidad', on_delete=models.PROTECT)
    sesiones = models.IntegerField(null=True,  blank=True)
    duracion = models.CharField(max_length=20, null=True,  blank=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(null=True,  blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        especialidad = self.especialidad.nombre if self.especialidad else 'Sin especialidad asignada'
        return f"{self.nombre} - {especialidad}"

