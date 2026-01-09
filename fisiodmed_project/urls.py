
from django.contrib import admin
from django.urls import include, path
from apps.autenticacion import views as autenticacion_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', autenticacion_views.login_view, name='login'),
    path('autenticacion/', include('apps.autenticacion.urls')),
    path('citas/', include('apps.citas.urls')),
    path('especialidades/', include('apps.especialidades.urls')),
    path('inicio/', include('apps.inicio.urls')),
    path('pacientes/', include('apps.pacientes.urls')),
    path('pagos/', include('apps.pagos.urls')),
    path('servicios/', include('apps.servicios.urls')),
    path('usuarios/', include('apps.usuarios.urls')),
    path('medicos/', include('apps.medicos.urls')),
]
