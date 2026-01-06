from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from apps.pacientes.models import Paciente
from apps.pacientes.models import Antecedentes
from datetime import date
from django.contrib import messages
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
@user_passes_test(roles_permitidos(['Secretaria', 'Medico', 'Administrador']))
def registrar_paciente(request):
    if request.method == 'POST':
        num_doc = request.POST.get('txtNumDoc')
        email = request.POST.get('txtEmail')

        # Validación
        if Paciente.objects.filter(num_doc=num_doc).exists():
            messages.error(request, 'Ya existe un paciente con ese número de documento.')
            return redirect('tabla_pacientes')
        
        if email and Paciente.objects.filter(email__iexact=email).exists():
            messages.error(request, 'Ya existe un paciente con ese correo electrónico.')
            return redirect('tabla_pacientes')

        fecha_nac = request.POST.get('txtFechNacimiento')
        edad = None

        if fecha_nac:
            fecha_nac = date.fromisoformat(fecha_nac)
            hoy = date.today()
            edad = hoy.year - fecha_nac.year - (
                (hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day)
            )

        Paciente.objects.create(
            nombres=request.POST.get('txtNombres'),
            apellidos=request.POST.get('txtApellidos'),
            num_doc=num_doc,
            email=email,
            telefono=request.POST.get('txtTelefono'),
            fecha_nac=fecha_nac,
            edad=edad,
            sexo=request.POST.get('txtSexo'),
            tipo_sangre=request.POST.get('txtTipoSangre'),
            direccion=request.POST.get('txtDireccion'),
            estado_civil=request.POST.get('txtEstadoCivil'),
        )

        messages.success(request, 'Paciente registrado correctamente.')
        return redirect('tabla_pacientes')

    return redirect('tabla_pacientes')

@login_required
@user_passes_test(roles_permitidos(['Secretaria', 'Medico', 'Administrador']))
def editar_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)

    if request.method == 'POST':
        num_doc = request.POST.get('txtNumDoc')
        email = request.POST.get('txtEmail')

        # Validar número de documento 
        if Paciente.objects.filter(num_doc=num_doc).exclude(id=paciente.id).exists():
            messages.error(request, 'Ya existe otro paciente con ese número de documento.')
            return redirect('editar_paciente', paciente_id=paciente.id)

        # Validar email
        if email and Paciente.objects.filter(email__iexact=email).exclude(id=paciente.id).exists():
            messages.error(request, 'Ya existe otro paciente con ese correo.')
            return redirect('editar_paciente', paciente_id=paciente.id)

        paciente.nombres = request.POST.get('txtNombres')
        paciente.apellidos = request.POST.get('txtApellidos')
        paciente.num_doc = num_doc
        paciente.email = email
        paciente.telefono = request.POST.get('txtTelefono')

        fecha_nac = request.POST.get('txtFechNacimiento')
        if fecha_nac:
            fecha_nac = date.fromisoformat(fecha_nac)
            hoy = date.today()
            paciente.edad = hoy.year - fecha_nac.year - (
                (hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day)
            )
            paciente.fecha_nac = fecha_nac
        else:
            paciente.fecha_nac = None
            paciente.edad = None

        paciente.sexo = request.POST.get('txtSexo')
        paciente.tipo_sangre = request.POST.get('txtTipoSangre')
        paciente.direccion = request.POST.get('txtDireccion')
        paciente.estado_civil = request.POST.get('txtEstadoCivil')

        paciente.save()
        messages.success(request, 'Paciente actualizado correctamente.')
        return redirect('tabla_pacientes')

    return render(request, 'pacientes/editar_paciente.html', {'paciente': paciente})



@login_required
@user_passes_test(roles_permitidos(['Secretaria', 'Medico', 'Administrador']))
def eliminar_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    paciente.delete()
    messages.success(request, 'Paciente eliminado correctamente.')
    return redirect('tabla_pacientes')


