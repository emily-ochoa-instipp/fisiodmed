from django.contrib.auth.models import Group, User
from apps.usuarios.models import Usuario
from apps.pacientes.models import Paciente
from apps.medicos.models import Medico
from apps.especialidades.models import Especialidad
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "first_name", "last_name", "groups", "date_joined"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]

class UsuarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Usuario
        fields = ["url", "num_doc", "telefono", "rol"]

class PacienteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Paciente
        fields = ["url", "fecha_nac", "edad", "sexo", "tipo_sangre", "direccion", "estado_civil"]

class MedicoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Medico
        fields = ["url", "especialidad", "direccion"]

class EspecialidadSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Especialidad
        fields = ["url", "nombre"]