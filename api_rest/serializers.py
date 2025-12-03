from django.contrib.auth.models import Group, User
from rest_framework import serializers
from apps.especialidades.models import Especialidad
from apps.citas.models import Cita
from apps.pacientes.models import Paciente 

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "first_name", "last_name", "groups", "date_joined"]

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]

class especialidadSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Especialidad
        fields = ["url", "name"]

class citaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cita
        fields = ["url", "paciente", "especialidad", "medico", "motivo", "servicio", "fecha", "hora", "duracion"]

class pacientesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Paciente
        fields = ["url", "usuario", "fecha_nac", "edad", "sexo", "tipo_sangre", "direccion", "estado_civil"]