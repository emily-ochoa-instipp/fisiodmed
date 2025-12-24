from django.urls import path
from . import views

urlpatterns = [
    # Vistas de pagos
    path('editar_pago/<int:id>/', views.editar_pago, name='editar_pago'),
    path('tabla_pagos/', views.tabla_pagos, name='tabla_pagos'),
]
