from django.urls import path
from . import views

urlpatterns = [
    path('listar_usuarios/', views.tabla_usuarios, name='tabla_usuarios'),
    path('registrar/', views.registrar_usuario, name='registrar_usuario'),

    path('usuarios/editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('profile/', views.profile, name='profile'),
]


