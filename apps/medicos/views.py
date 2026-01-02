from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from apps.medicos.models import Medico
from apps.especialidades.models import Especialidad
from apps.usuarios.models import Usuario
from django.contrib.auth.models import User
from apps.usuarios.decorators import roles_permitidos


# Create your views here.

@login_required
@user_passes_test(roles_permitidos(['Administrador']))
def tabla_medicos(request):
    medicos = Medico.objects.all()
    especialidades = Especialidad.objects.all() 
    return render(request, 'medicos/tabla_medicos.html', {
        'medicos': medicos,
        'especialidades': especialidades,
    })
@login_required
@user_passes_test(roles_permitidos(['Administrador']))
def registrar_medico(request):
    if request.method == 'POST':
        nombres = request.POST['txtNombres']
        apellidos = request.POST['txtApellidos']
        especialidad_id = request.POST['txtEspecialidad']
        num_doc = request.POST['txtNumDoc']
        telefono = request.POST['txtTelefono']
        email = request.POST['txtEmail']
        direccion = request.POST['txtDireccion']

        especialidad_obj = Especialidad.objects.get(id=especialidad_id)
    
        #user
        userCreate = User.objects.create_user(
            first_name=nombres,
            last_name=apellidos,
            username=num_doc, 
            email=email,
            password='12345' 
        )

        # Usuario 
        usuarioCreate = Usuario.objects.create(
            user=userCreate,
            rol='Medico',
            telefono=telefono,
            num_doc=num_doc,
        )

        # médico 
        Medico.objects.create(
            usuario=usuarioCreate,
            especialidad=especialidad_obj,
            direccion=direccion
        )

        return redirect('tabla_medicos')
    return render(request, 'medicos/tabla_medicos.html')

@login_required
@user_passes_test(roles_permitidos(['Administrador']))
def editar_medico(request, medico_id):
    medico = Medico.objects.get(id=medico_id)
    especialidades = Especialidad.objects.all()

    if request.method == 'POST':
        usuario = medico.usuario
        user = usuario.user

        # user
        user.first_name = request.POST['txtNombres']
        user.last_name = request.POST['txtApellidos']
        user.email = request.POST['txtEmail']
        user.save()

        # usuario
        usuario.num_doc = request.POST['txtNumDoc']
        usuario.telefono = request.POST['txtTelefono']
        usuario.save()

        # medico
        #medico.num_doc = request.POST.get('txtNumDoc') or None
        medico.direccion = request.POST.get('txtDireccion') or None
        especialidad_id = request.POST.get('txtEspecialidad')
        if especialidad_id:
            medico.especialidad = Especialidad.objects.get(id=especialidad_id)
        else:
            medico.especialidad = None
        medico.save()
        

        return redirect('tabla_medicos')

    return render(request, 'medicos/editar_medico.html', {'medico': medico, 'especialidades': especialidades})

@login_required
@user_passes_test(roles_permitidos(['Administrador']))
def eliminar_medico(request, medico_id):
    medico = get_object_or_404(Medico, id=medico_id)
    usuario = medico.usuario  
    user = usuario.user
    
    medico.delete()  
    usuario.delete() 
    user.delete()  
    
    return redirect('tabla_medicos')

