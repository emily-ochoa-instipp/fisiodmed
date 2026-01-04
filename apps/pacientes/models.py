from django.db import models
from apps.usuarios.models import Usuario

# Create your models here.

class Paciente(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    num_doc = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True, unique=True)
    fecha_nac = models.DateField(null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    sexo = models.CharField(max_length=10, null=True, blank=True)
    tipo_sangre = models.CharField(max_length=3, null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    estado_civil = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

