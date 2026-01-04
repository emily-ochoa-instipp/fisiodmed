from django.urls import path
from . import views

from .views import citas_calendario


urlpatterns = [
    # Vistas de citas
    path('calendar/', views.calendar, name='calendar'),
    path('listar_citas/', views.tabla_citas, name='tabla_citas'),
    path('citas/registrar/', views.registrar_cita, name='registrar_cita'),
    path('citas/editar/<int:cita_id>/', views.editar_cita, name='editar_cita'),
    path('citas/eliminar/<int:cita_id>/', views.eliminar_cita, name='eliminar_cita'),

    path('calendario/', views.citas_calendario, name='citas_calendario'),
]



