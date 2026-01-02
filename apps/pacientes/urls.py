from django.urls import path
from . import views

urlpatterns = [
    # Vistas de pacientes

    path('listar_pacientes/', views.tabla_pacientes, name='tabla_pacientes'),
    path('pacientes/registrar/', views.registrar_paciente, name='registrar_paciente'),
    path('pacientes/editar/<int:paciente_id>/', views.editar_paciente, name='editar_paciente'),
    path('pacientes/eliminar/<int:paciente_id>/', views.eliminar_paciente, name='eliminar_paciente'),
]
