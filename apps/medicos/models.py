from django.db import models
from apps.usuarios.models import Usuario
from apps.especialidades.models import Especialidad

# Create your models here.  

class Medico (models.Model):
    usuario = models.OneToOneField('usuarios.Usuario', on_delete=models.CASCADE)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.PROTECT)
    direccion = models.CharField(max_length=255, null=True,  blank=True)
    activo = models.BooleanField(default=True)


    def __str__(self):
        especialidad = self.especialidad.nombre if self.especialidad else 'Sin especialidad asignada'
        return f"{self.usuario.user.first_name} {self.usuario.user.last_name} - {especialidad}"

    
    