from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from apps.especialidades.models import Especialidad
from apps.citas.models import Cita
from apps.medicos.models import Medico
from apps.servicios.models import Servicio
from apps.pacientes.models import Paciente
from datetime import datetime
from apps.usuarios.decorators import roles_permitidos

# Create your views here.

@login_required
@user_passes_test(roles_permitidos(['Secretaria', 'Medico','Administrador', 'Recepcionista']))
def calendar(request):
    return render(request, 'citas/calendar.html')

# Create your views here.

@login_required
@user_passes_test(roles_permitidos(['Secretaria', 'Medico','Administrador', 'Recepcionista']))
def tabla_citas(request):
    citas = Cita.objects.all()
    pacientes = Paciente.objects.all()
    medicos = Medico.objects.all()
    especialidades = Especialidad.objects.all()
    servicios = Servicio.objects.all()

    return render(request, 'citas/tabla_citas.html', {
        'citas': citas,
        'pacientes': pacientes,
        'medicos': medicos,
        'especialidades': especialidades,
        'servicios': servicios
    })

@login_required
@user_passes_test(roles_permitidos(['Administrador', 'Recepcionista']))
def registrar_cita(request):
    if request.method == 'POST':
        fecha_str = request.POST.get('txtFecha')  
        fecha = datetime.strptime(fecha_str, '%m/%d/%Y').date()

        hora_str = request.POST.get('txtHora')  
        hora = datetime.strptime(hora_str, '%I:%M %p').time()

        paciente_id = request.POST['txtPaciente']
        especialidad_id = request.POST['txtEspecialidad']
        medico_id = request.POST['txtMedico']
        motivo = request.POST['txtMotivo']
        servicio_id = request.POST['txtServicio']
        #fecha = request.POST['txtFecha']
        #hora = request.POST['txtHora']
        #frecuencia = request.POST['txtEstadoCivil']
        #valido_hasta = request.POST['txtNumDoc']
        duracion = request.POST['txtDuracion']

        paciente_obj = Paciente.objects.get(id=paciente_id)
        especialidad_obj = Especialidad.objects.get(id=especialidad_id)
        medico_obj = Medico.objects.get(id=medico_id)
        servicio_obj = Servicio.objects.get(id=servicio_id)

        Cita.objects.create(
            paciente=paciente_obj,
            especialidad=especialidad_obj,
            medico=medico_obj,
            servicio=servicio_obj,
            motivo=motivo,
            fecha=fecha,
            hora=hora,
            duracion=duracion           
        )
        return redirect('tabla_citas')
    return render(request, 'citas/tabla_citas.html')

@login_required
@user_passes_test(roles_permitidos(['Administrador', 'Recepcionista']))
def editar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    pacientes = Paciente.objects.all()
    especialidades = Especialidad.objects.all()
    medicos = Medico.objects.all()
    servicios = Servicio.objects.all()

    if request.method == 'POST':
        # Obtener datos del formulario
        fecha_str = request.POST.get('txtFecha')
        hora_str = request.POST.get('txtHora')
        paciente_id = request.POST.get('txtPaciente')
        especialidad_id = request.POST.get('txtEspecialidad')
        medico_id = request.POST.get('txtMedico')
        motivo = request.POST.get('txtMotivo')
        duracion = request.POST.get('txtDuracion')
        servicio_id = request.POST.get('txtServicio')

        # Parsear fecha y hora si vienen
        if fecha_str:
            cita.fecha = datetime.strptime(fecha_str, '%m/%d/%Y').date()
        if hora_str:
            cita.hora = datetime.strptime(hora_str, '%I:%M %p').time()

        # Actualizar relaciones FK
        if paciente_id:
            cita.paciente = Paciente.objects.get(id=paciente_id)
        if especialidad_id:
            cita.especialidad = Especialidad.objects.get(id=especialidad_id)
        if medico_id:
            cita.medico = Medico.objects.get(id=medico_id)
        if servicio_id:
            cita.servicio = Servicio.objects.get(id=servicio_id)

        cita.motivo = motivo
        cita.duracion = duracion

        cita.save()

        return redirect('tabla_citas')
    return render(request, 'citas/editar_cita.html', {
        'cita': cita,
        'pacientes': pacientes,
        'especialidades': especialidades,
        'medicos': medicos,
        'servicios': servicios,
    })


@login_required
@user_passes_test(roles_permitidos(['Administrador', 'Recepcionista']))

def eliminar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    cita.delete()
    return redirect('tabla_citas')