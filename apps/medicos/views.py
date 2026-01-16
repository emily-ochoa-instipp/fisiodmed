from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from apps.medicos.models import Medico
from apps.especialidades.models import Especialidad
from apps.usuarios.models import Usuario
from django.contrib.auth.models import User, Group
from apps.usuarios.decorators import roles_permitidos, validar_grupos_existentes
from django.contrib import messages



# Create your views here.

@login_required
@user_passes_test(roles_permitidos(['Administrador', 'Recepcionista']))
def tabla_medicos(request):
    medicos = Medico.objects.order_by('-activo')
    especialidades = Especialidad.objects.filter(activo=True)

    validar_grupos_existentes(request)
    
    return render(request, 'medicos/tabla_medicos.html', {
        'medicos': medicos,
        'especialidades': especialidades,
    })
@login_required
@user_passes_test(roles_permitidos(['Administrador']))
def registrar_medico(request):
    validar_grupos_existentes(request)

    if request.method == 'POST':
        if not Group.objects.exists():
            messages.error(
                request,
                "No existe rol o grupo médico creado en el admin."
            )
            return redirect('tabla_medicos')
        
        nombres = request.POST['txtNombres']
        apellidos = request.POST['txtApellidos']
        especialidad_id = request.POST['txtEspecialidad']
        num_doc = request.POST['txtNumDoc']
        telefono = request.POST['txtTelefono']
        email = request.POST['txtEmail']
        direccion = request.POST['txtDireccion']

        #  VALIDACIONES 
        if User.objects.filter(username=num_doc).exists():
            messages.error(request, 'Ya existe un usuario con ese número de documento.')
            return redirect('tabla_medicos')

        if Usuario.objects.filter(num_doc=num_doc).exists():
            messages.error(request, 'Ese número de documento ya está registrado.')
            return redirect('tabla_medicos')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Ese correo ya está registrado.')
            return redirect('tabla_medicos')

        especialidad = get_object_or_404(Especialidad,id=especialidad_id,activo=True)

    
        #user
        user = User.objects.create_user(
            first_name=nombres,
            last_name=apellidos,
            username=num_doc, 
            email=email,
            password=num_doc, 
        )

        user.is_active = True   # Activo por defecto
        user.save()

        
        # ASIGNAR GRUPO MEDICO
        try:
            grupo_medico = Group.objects.get(name='Medico')
        except Group.DoesNotExist:
            messages.error(
                request,
                "El rol Médico no existe. Contacte al administrador."
            )
            user.delete()  
            return redirect('tabla_medicos')
        user.groups.add(grupo_medico)

        # 3️Obtener Usuario creado por signal
        usuario = user.usuario
        usuario.telefono = telefono
        usuario.num_doc = num_doc
        usuario.save()
        
        # médico 
        Medico.objects.create(
            usuario=usuario,
            especialidad=especialidad,
            direccion=direccion,
        )
        messages.success(request, 'Medico registrado correctamente.')
        return redirect('tabla_medicos')
    return redirect('tabla_medicos')

@login_required
@user_passes_test(roles_permitidos(['Administrador']))
def editar_medico(request, medico_id):
    medico = get_object_or_404(Medico, id=medico_id)
    especialidades = Especialidad.objects.filter(activo=True)

    validar_grupos_existentes(request)

    if request.method == 'POST':
        usuario = medico.usuario
        user = usuario.user

        nombres = request.POST['txtNombres']
        apellidos = request.POST['txtApellidos']
        email = request.POST['txtEmail']
        num_doc = request.POST['txtNumDoc']
        telefono = request.POST['txtTelefono']
        direccion = request.POST['txtDireccion']
        especialidad_id = request.POST['txtEspecialidad']

        if 'estado' in request.POST:
            user.is_active = True
        else:
            user.is_active = False

        #  VALIDACIONES
        if User.objects.filter(username=num_doc).exclude(id=user.id).exists():
            messages.error(request, 'Ese número de documento ya está en uso.')
            return redirect('tabla_medicos')

        if User.objects.filter(email=email).exclude(id=user.id).exists():
            messages.error(request, 'Ese correo ya está en uso.')
            return redirect('tabla_medicos')

        # user
        user.first_name = nombres
        user.last_name = apellidos
        user.email = email
        user.username = num_doc
        user.save()

        # usuario
        usuario.num_doc = num_doc
        usuario.telefono = telefono
        usuario.save()

        # medico
        medico.direccion = direccion
        medico.especialidad = get_object_or_404(
            Especialidad,
            id=especialidad_id,
            activo=True
        )
        medico.save()

        messages.success(request, 'Médico actualizado correctamente.')
        return redirect('tabla_medicos')

    return render(request, 'medicos/editar_medico.html', {
        'medico': medico,
        'especialidades': especialidades
    })


@login_required
@user_passes_test(roles_permitidos(['Administrador']))
def eliminar_medico(request, medico_id):
    medico = get_object_or_404(Medico, id=medico_id)
    user = medico.usuario.user

    user.is_active = False
    user.save() 
    messages.success(request, 'Medico desactivado correctamente.')
    return redirect('tabla_medicos')

