
def usuario_actual(request):
    usuario = None
    if request.user.is_authenticated:
        usuario = getattr(request.user, 'usuario', None)
    return {'usuario': usuario}
