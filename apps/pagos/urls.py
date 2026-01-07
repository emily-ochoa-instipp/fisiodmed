from django.urls import path
from . import views

urlpatterns = [
    # Vistas de pagos
    # path('listar_pagos/', views.tabla_pagos, name='tabla_pagos'),
    path('pagos/registrar/<int:cita_id>/', views.registrar_pago, name='registrar_pago'),
    path('pagos/editar/<int:pago_id>/', views.editar_pago, name='editar_pago'),
    path('pagos/eliminar/<int:pago_id>/', views.eliminar_pago, name='eliminar_pago'),
]
