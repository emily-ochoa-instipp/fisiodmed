from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

from django.contrib.auth.forms import PasswordResetForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('inicio')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip().lower()
        password = request.POST.get('password', '')

        if not username or not password:
            messages.error(request, 'Ingrese usuario y contraseña.')
            return redirect('login')

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, 'Usuario o contraseña incorrectos')
            return redirect('login')

        if not user.is_active:
            messages.error(request, 'Cuenta desactivada.')
            return redirect('login')

        login(request, user)

        return redirect('inicio')

    return render(request, 'autenticacion/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)

        if form.is_valid():
            form.save(
                request=request,
                use_https=True,
                from_email=settings.EMAIL_HOST_USER,
                email_template_name='autenticacion/password_reset_email.html'
            )
            messages.success(
                request,
                'Si el correo existe, se enviaron las instrucciones.'
            )
            return redirect('login')
    else:
        form = PasswordResetForm()

    return render(request, 'autenticacion/password_reset_form.html', {
        'form': form
    })
