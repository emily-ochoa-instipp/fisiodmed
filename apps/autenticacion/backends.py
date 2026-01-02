from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q
from apps.usuarios.models import Usuario


class MultiFieldAuthBackend(ModelBackend):
    """
    Custom authentication backend that allows authentication using
    username, email, or cedula.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
       
        # Buscar por: username, email o cédula
        try:
            # Busca por username
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            pass

         # Busca por email
        try:
            user = User.objects.get(email__iexact=username)
            if user.check_password(password):
                return user
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            pass
        
        # Busca por cédula en el perfil
        try:
            usuario = Usuario.objects.get(num_doc__iexact=username)
            user = usuario.user
            if user.check_password(password):
                return user
        except Usuario.DoesNotExist:
            return None
        
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None