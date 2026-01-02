from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from apps.especialidades.models import Especialidad
from apps.citas.models import Cita
from apps.pacientes.models import Paciente
from .serializers import UserSerializer,GroupSerializer,especialidadSerializer,pacientesSerializer,citaSerializer

# Create your views here.


from apps.autenticacion.models import Profile
from rest_framework import permissions, viewsets

from .serializers import GroupSerializer, UserSerializer, ProfileSerializer

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    #permission_classes = [permissions.IsAuthenticated]



class especialidadViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Especialidad.objects.all()
    serializer_class = especialidadSerializer
    #permission_classes = [permissions.IsAuthenticated]

class citaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Cita.objects.all()
    serializer_class = citaSerializer
    #permission_classes = [permissions.IsAuthenticated]

class pacientesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Paciente.objects.all()
    serializer_class = pacientesSerializer
    #permission_classes = [permissions.IsAuthenticated]
class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    #permission_classes = [permissions.IsAuthenticated]

class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    #permission_classes = [permissions.IsAuthenticated]
