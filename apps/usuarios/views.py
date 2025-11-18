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
    if request.method == 'POST':

        first_name_ = request.POST['txtNombres']
        last_name_= request.POST['txtApellidos']
        email_ = request.POST['txtEmail']
        num_doc_ = request.POST['txtNumDoc']
        username_ = request.POST['txtUsername']
        password_ = request.POST['txtPassword']
        rol_ = request.POST['txtRol']
        telefono_ = request.POST['txtTelefono']

        users = User.objects.filter(
            Q(username__iexact=username_) |
            Q(email__iexact=email_)
        )

        usuarios = Usuario.objects.filter(
            Q(num_doc__iexact=num_doc_)
        )

        if users.exists() or usuarios.exists():
            return render(request, 'usuarios/tabla_usuarios.html', {
                'error': 'Ya existe un usuario con ese nombre de usuario, email o cédula'
            })
        else:
            userCreate = User.objects.create_user(
                first_name=first_name_, last_name=last_name_, email=email_, username=username_, password=password_)

            usuarioCreate = Usuario.objects.create(
                user=userCreate, telefono=telefono_, num_doc=num_doc_, rol=rol_)
            
            if rol_ == 'Paciente':
                Paciente.objects.create(
                    usuario=usuarioCreate,
                    fecha_nac=None,
                    edad=None,
                    sexo=None,
                    tipo_sangre=None,
                    #num_doc=num_doc_,  
                    direccion=None,
                    estado_civil=None
                )
            if rol_ == 'Medico':
                Medico.objects.create(
                    usuario=usuarioCreate,
                    direccion=None,
                    especialidad=None,
                )

        return redirect('tabla_usuarios')
    
    return render(request, 'usuarios/tabla_usuarios.html')

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
def profile(request):
    return render(request, 'usuarios/profile.html')

