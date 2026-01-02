from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from apps.pacientes.models import Paciente
from datetime import date
from apps.usuarios.models import Usuario
from django.contrib.auth.models import User
from apps.usuarios.decorators import roles_permitidos

# Create your views here.

@login_required
@user_passes_test(roles_permitidos(['Secretaria', 'Medico','Administrador']))
def tabla_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'pacientes/tabla_pacientes.html', {
        'pacientes': pacientes
    })
@login_required
@user_passes_test(roles_permitidos(['Secretaria', 'Medico','Administrador']))
def registrar_paciente(request):
    if request.method == 'POST':
        nombres = request.POST['txtNombres']
        apellidos = request.POST['txtApellidos']
        fecha_nac = request.POST['txtFechNacimiento']
        edad = request.POST['txtEdad']
        sexo = request.POST['txtSexo']
        tipo_sangre = request.POST['txtTipoSangre']
        direccion = request.POST['txtDireccion']
        estado_civil = request.POST['txtEstadoCivil']
        num_doc = request.POST['txtNumDoc']
        telefono = request.POST['txtTelefono']
        email = request.POST['txtEmail']

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
            rol='Paciente',
            telefono=telefono,
            num_doc=num_doc,
        )

        Paciente.objects.create(
            usuario=usuarioCreate, 
            fecha_nac = fecha_nac,
            edad = edad,
            sexo = sexo,
            tipo_sangre = tipo_sangre,
            direccion = direccion,
            estado_civil = estado_civil
        )
        return redirect('tabla_pacientes')
    return render(request, 'pacientes/tabla_pacientes.html')

@login_required
@user_passes_test(roles_permitidos(['Secretaria', 'Medico','Administrador']))
def editar_paciente(request, paciente_id):
    paciente = Paciente.objects.get(id=paciente_id)

    if request.method == 'POST':
        usuario = paciente.usuario
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

        # paciente
        fecha_nac_str = request.POST.get('txtFechNacimiento')
        if fecha_nac_str:
            fecha_nac = date.fromisoformat(fecha_nac_str)
            paciente.fecha_nac = fecha_nac

            # Calcular edad 
            hoy = date.today()
            edad = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
            paciente.edad = edad

        else:
            paciente.fecha_nac = None
            paciente.edad = None
        #paciente.fecha_nac = request.POST.get('txtFechNacimiento') or None
        #paciente.edad = request.POST.get('txtEdad') or None
        paciente.sexo = request.POST.get('txtSexo') or None
        paciente.tipo_sangre = request.POST.get('txtTipoSangre') or None
        # paciente.num_doc = request.POST.get('txtNumDoc') or None
        paciente.direccion = request.POST.get('txtDireccion') or None
        paciente.estado_civil = request.POST.get('txtEstadoCivil') or None

        paciente.save()
        

        return redirect('tabla_pacientes')

    return render(request, 'pacientes/editar_paciente.html', {'paciente': paciente})

@login_required
@user_passes_test(roles_permitidos(['Secretaria', 'Medico','Administrador']))
def eliminar_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    usuario = paciente.usuario  
    user = usuario.user
    
    paciente.delete()  
    usuario.delete()   
    user.delete()
    
    return redirect('tabla_pacientes')

