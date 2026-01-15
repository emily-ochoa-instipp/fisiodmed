from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from apps.especialidades.models import Especialidad
from apps.usuarios.decorators import roles_permitidos
from django.contrib import messages
# Create your views here.

@login_required
@user_passes_test(roles_permitidos(['Administrador', 'Recepcionista']))
def tabla_especialidades(request):
    especialidades = Especialidad.objects.order_by('-activo', 'nombre')
    return render(request, 'especialidades/tabla_especialidades.html', {
        'especialidades': especialidades
    })

def registrar_especialidad(request):
    if request.method == 'POST':
        nombre = request.POST['txtNombre']

        Especialidad.objects.create(
            nombre = nombre,
            activo=True
        )
        messages.success(request, 'Especialidad registrada correctamente.')
        return redirect('tabla_especialidades')
    return redirect('tabla_especialidades')

@login_required
@user_passes_test(roles_permitidos(['Administrador']))
def editar_especialidad(request, especialidad_id):
    especialidad = Especialidad.objects.get(id=especialidad_id)

    if request.method == 'POST':
        especialidad.nombre = request.POST.get('txtNombre')
        especialidad.activo = 'activo' in request.POST
        especialidad.save()

        messages.success(request, 'Especialidad actualizada correctamente.')
        return redirect('tabla_especialidades')

    return render(request, 'especialidades/editar_especialidad.html', {'especialidad': especialidad})

@login_required
@user_passes_test(roles_permitidos(['Administrador']))
def eliminar_especialidad(request, especialidad_id):
    especialidad = get_object_or_404(Especialidad, id=especialidad_id)

    especialidad.activo = False
    especialidad.save()
    messages.success(request,'Especialidad desactivada correctamente.')

    return redirect('tabla_especialidades')
