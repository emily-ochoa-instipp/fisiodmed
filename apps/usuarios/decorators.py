from django.contrib.auth.models import Group
from django.contrib import messages
from django.shortcuts import redirect


def roles_permitidos(roles):
    def check(user):
        # Si no hay grupos, permitir acceso para mostrar alerta
        if not Group.objects.exists():
            return True

        return (
            user.is_authenticated and
            (user.is_superuser or user.groups.filter(name__in=roles).exists())
        )
    return check


def validar_grupos_existentes(request):
    if (
        request.user.is_authenticated and
        not Group.objects.exists() and
        not request.session.get('alerta_grupos_mostrada', False)
    ):
        messages.error(
            request,
            "Aún no se han creado los grupos de usuarios en el administrador."
        )
        request.session['alerta_grupos_mostrada'] = True
