from django.db import models

# Create your models here.
class Especialidad (models.Model):
    nombre = models.CharField(max_length=225)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre