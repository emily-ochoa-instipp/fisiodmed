from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from apps.usuarios.models import Usuario
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.contrib.auth import update_session_auth_hash #funcion para evitar q se cierre la sesion luego de cambiar la contraseña
from django.urls import reverse
from django.contrib import messages

from django.contrib.auth import password_validation 
from django.core.exceptions import ValidationError
from apps.usuarios.decorators import roles_permitidos

# Create your views here.

@login_required
@user_passes_test(roles_permitidos(['Secretaria', 'Presidenta', 'Administrador']))

def tabla_usuarios(request):
    usuarios = Usuario.objects.all()
    roles = Group.objects.all() 
    return render(request, 'usuarios/tabla_usuarios.html', {
        'usuarios': usuarios, 'roles': roles
    })

@login_required
@user_passes_test(roles_permitidos(['Secretaria', 'Presidenta', 'Administrador']))
def registrar_usuario(request):
    if request.method == 'POST':
            first_name_ = request.POST.get('txtNombres')
            last_name_ = request.POST.get('txtApellidos')
            email_ = request.POST.get('txtEmail')
            num_doc_ = request.POST.get('txtNumDoc')
            username_ = request.POST.get('txtUsername')
            password_ = request.POST.get('txtPassword')
            rol_ = request.POST.get('txtRol')
            telefono_ = request.POST.get('txtTelefono')

            # Verificar duplicados
            if User.objects.filter(username__iexact=username_).exists():
                messages.error(request, 'El nombre de usuario ya existe.')
                return redirect('tabla_usuarios')

            if User.objects.filter(email__iexact=email_).exists():
                messages.error(request, 'El correo electrónico ya está registrado.')
                return redirect('tabla_usuarios')

            if Usuario.objects.filter(num_doc__iexact=num_doc_).exists():
                messages.error(request, 'El número de documento ya está registrada.')
                return redirect('tabla_usuarios')
            
            # Crear el usuario base
            user = User.objects.create_user(
                first_name=first_name_,
                last_name=last_name_,
                email=email_,
                username=username_,
                password=password_
            )

            user.is_active = True   # Activo por defecto
            user.save()

            # asignar grupo (ROL)
            grupo = Group.objects.get(name=rol_)
            user.groups.add(grupo)

            #perfil Usuario se crea automáticamente por signals.py
            usuario = user.usuario
            usuario.telefono = telefono_
            usuario.num_doc = num_doc_
            usuario.save()
            messages.success(request, 'Usuario registrado correctamente.')
            return redirect('tabla_usuarios')
    
    return redirect('tabla_usuarios')

@login_required
@user_passes_test(roles_permitidos(['Secretaria', 'Presidenta', 'Administrador']))

def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        user = usuario.user
        usuario.user.first_name = request.POST.get('txtNombres')
        usuario.user.last_name = request.POST.get('txtApellidos')
        usuario.user.email = request.POST.get('txtEmail')
        usuario.user.username = request.POST.get('txtUsername')
        if 'estado' in request.POST:
            user.is_active = True
        else:
            user.is_active = False

        # cambiar rol (grupo)
        rol_ = request.POST.get('txtRol')
        grupo = Group.objects.get(name=rol_)
        user.groups.clear()
        user.groups.add(grupo)

        usuario.num_doc = request.POST.get('txtNumDoc')
        usuario.telefono = request.POST.get('txtTelefono')

        usuario.user.save()
        usuario.save()
        messages.success(request, 'Usuario actualizado correctamente.')    
        return redirect('tabla_usuarios')
    roles = Group.objects.all()
    return render(request, 'usuarios/editar_usuario.html', {'usuario': usuario, 'roles': roles})

@login_required
@user_passes_test(roles_permitidos(['Secretaria', 'Presidenta', 'Administrador']))

def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    user = usuario.user
    user.delete()
    messages.success(request, 'Usuario eliminado correctamente.')
    return redirect('tabla_usuarios')

@login_required
@user_passes_test(roles_permitidos(['Secretaria', 'Presidenta', 'Administrador', 'Socia']))

def profile(request):
    usuario = Usuario.objects.get(user=request.user)

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        # URL base
        profile_url = reverse('profile')       

        if form_type == 'perfil':
            # actualizar campos user
            user = request.user
            user.first_name = request.POST.get('txtNombres')
            user.last_name = request.POST.get('txtApellidos')
            user.email = request.POST.get('txtEmail')
            user.save()

            # actualizar campos de modelo usuario
            usuario.telefono = request.POST.get('txtTelefono')
            usuario.num_doc = request.POST.get('txtNumDoc')

            if 'foto' in request.FILES:
                usuario.foto = request.FILES['foto']

            usuario.save()
        
            messages.success(request, 'Datos del perfil actualizados correctamente.')
            return redirect(profile_url + '#perfil')
    
        elif form_type == 'cuenta':
            # Obtener nuevo nombre de usuario y confirmación de contraseña
            nuevo_usuario = request.POST.get('txtNewUsername')
            confirm_password = request.POST.get('txtPassword')

            # Verificar si realmente hay un cambio de nombre de usuario
            if nuevo_usuario and nuevo_usuario != request.user.username:     

                # Verificar si el usuario ingresó la contraseña correcta
                if not request.user.check_password(confirm_password):
                    messages.error(request, 'La contraseña no es correcta. No se pudo cambiar el nombre de usuario.')
                    return redirect(profile_url + '#cuenta')

                # Verificar si el nombre de usuario ya está en uso
                if User.objects.filter(username=nuevo_usuario).exclude(pk=request.user.pk).exists():
                    messages.error(request, 'El nombre de usuario ya está en uso.')
                    return redirect(profile_url + '#cuenta')

                # Actualizar nombre de usuario
                request.user.username = nuevo_usuario
                request.user.save()

                messages.success(request, 'Nombre de usuario actualizado correctamente.')
                # Redirige y usa el hash para volver al tab 'cuenta'
                return redirect(profile_url + '#cuenta')
            
            else:
                messages.warning(request, 'No se ingresó un nuevo nombre de usuario o es igual al actual.')
                return redirect(profile_url + '#cuenta')


        elif form_type == 'contrasena':
            current_password = request.POST.get('txtPassword')
            new_password = request.POST.get('txtNewPassword')
            confirm_new_password = request.POST.get('txtConfNewPass')
            
            # verificar coincidencia ntre nueva contraseña y la confirmacion
            if new_password != confirm_new_password:
                messages.error(request, 'La nueva contraseña y la confirmación no coinciden.')
                return redirect(profile_url + '#contrasena')

            # Verificar la contraseña actual
            if not request.user.check_password(current_password):
                messages.error(request, 'La contraseña actual no es correcta.')
                return redirect(profile_url + '#contrasena')

            # Reglas de Validación de Django
            try:
                password_validation.validate_password(new_password, user=request.user)
                
            except ValidationError as e:
                for error in e.messages:
                    messages.error(request, error)
                return redirect(profile_url + '#contrasena')

            # Cambiar la contraseña
            request.user.set_password(new_password)
            request.user.save()
            
            # Mantener la sesión de usuario activa 
            update_session_auth_hash(request, request.user)

            messages.success(request, 'Contraseña actualizada correctamente.')
            return redirect(profile_url + '#contrasena')
        
    return render(request, 'usuarios/profile.html', {'usuario': usuario})

@login_required
def no_permitido(request):
    return render(request, 'no_permitido.html')    
