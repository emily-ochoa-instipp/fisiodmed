from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.servicios.models import Servicio
from apps.especialidades.models import Especialidad
from django.contrib.auth.decorators import login_required, user_passes_test
from apps.usuarios.decorators import roles_permitidos
from django.contrib import messages


# Create your views here.

@login_required
@user_passes_test(roles_permitidos(['Administrador, Recepcionista']))
def tabla_servicios(request):
    servicios = Servicio.objects.all()
    especialidades = Especialidad.objects.all()
    return render(request, 'servicios/tabla_servicios.html', {
        'servicios': servicios,
        'especialidades': especialidades
    })

@user_passes_test(roles_permitidos(['Administrador']))
def registrar_servicio(request):
    especialidades = Especialidad.objects.all()
    if request.method == 'POST':
        nombre = request.POST['txtNombre']
        especialidad_id = request.POST['txtEspecialidad']
        sesiones = request.POST.get('txtSesiones') or None
        duracion = request.POST['txtDuracion']
        costo = request.POST['txtCosto']
        descripcion = request.POST.get('txtDescripcion')

        servicioCreate = Servicio.objects.create(
            nombre = nombre,
            especialidad_id = especialidad_id,
            sesiones = sesiones,
            duracion = duracion,
            costo = costo,
            descripcion = descripcion
        )
        messages.success(request, 'Servicio registrado correctamente.')
        return redirect('tabla_servicios')
    return render(request, 'servicios/tabla_servicios.html', {'especialidades': especialidades})

@user_passes_test(roles_permitidos(['Administrador']))
@login_required
def editar_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)
    especialidades = Especialidad.objects.all()

    if request.method == 'POST':
        servicio.nombre = request.POST.get('txtNombre')
        servicio.especialidad_id = request.POST.get('txtEspecialidad')
        servicio.sesiones = request.POST.get('txtSesiones') or None
        servicio.duracion = request.POST.get('txtDuracion')
        servicio.costo = request.POST.get('txtCosto')
        servicio.descripcion = request.POST.get('txtDescripcion')

        servicio.save()
        messages.success(request, 'Servicio actualizado correctamente.')
        return redirect('tabla_servicios')

    return render(request, 'servicios/editar_servicio.html', {'servicio': servicio, 'especialidades': especialidades})

@user_passes_test(roles_permitidos(['Administrador']))
@login_required
def eliminar_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)
    servicio.delete()  
    messages.success(request, 'Servicio eliminado correctamente.')
    return redirect('tabla_servicios')
