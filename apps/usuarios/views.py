from pyexpat.errors import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from apps.usuarios.models import Usuario
from django.contrib.auth.models import User
from django.db.models import Q
from apps.pacientes.models import Paciente
from apps.medicos.models import Medico
from apps.especialidades.models import Especialidad

# Create your views here.

@login_required
def tabla_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/tabla_usuarios.html', {
        'usuarios': usuarios
    })

def registrar_usuario(request):
    if request.method == "POST":
        rol = request.POST.get("txtRol")
        nombres = request.POST.get("txtNombres")
        apellidos = request.POST.get("txtApellidos")
        email = request.POST.get("txtEmail")
        telefono = request.POST.get("txtTelefono")
        num_doc = request.POST.get("txtNumDoc")
        username = request.POST.get("txtUsername")
        password = request.POST.get("txtPassword")
        estado = request.POST.get("txtEstado") == "on"

        # VALIDAR SI YA EXISTE EL USERNAME
        if User.objects.filter(username=username).exists():
            return render(request, "tabla_usuarios.html", {
                "error": "El nombre de usuario ya existe",
                "usuarios": Usuario.objects.all()
            })

        # CREAR USUARIO DJANGO
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=nombres,
            last_name=apellidos
        )

        # CREAR PERFIL
        Usuario.objects.create(
            user=user,
            rol=rol,
            telefono=telefono,
            num_doc=num_doc,
            estado=estado
        )

        messages.success(request, "Usuario registrado correctamente")
        return redirect("tabla_usuarios")

    # si entran por GET
    return redirect("tabla_usuarios")

@login_required
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        #user
        usuario.user.first_name = request.POST.get('txtNombres')
        usuario.user.last_name = request.POST.get('txtApellidos')
        usuario.user.email = request.POST.get('txtEmail')
        usuario.user.username = request.POST.get('txtUsername')
        usuario.user.set_password = request.POST.get('txtPassword')
        
        #usuario     
        usuario.rol = request.POST.get('txtRol')
        usuario.num_doc = request.POST.get('txtNumDoc')
        usuario.telefono = request.POST.get('txtTelefono')
        usuario.user.save()
        usuario.save()
        return redirect('tabla_usuarios')
    return render(request, 'usuarios/editar_usuario.html', {'usuario': usuario})

@login_required
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    user = usuario.user
    user.delete()
    return redirect('tabla_usuarios')

@login_required
def profile(request, usuario_id):
    return render(request, 'usuarios/profile.html')

