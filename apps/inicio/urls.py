from django.urls import path
from . import views

urlpatterns = [
    # Vistas de inicio
    path('inicio/', views.inicio, name='inicio'),
]
