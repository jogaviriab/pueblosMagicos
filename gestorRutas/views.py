from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from .models import Usuario

def crearUsuario(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        contrasena = request.POST.get('contrasena')
        confirmar_contrasena = request.POST.get('confirmar_contrasena')

        if Usuario.objects.filter(email=email).exists():
            return render(request, 'crearUsuario.html', {'mensaje': "Usuario ya existe" ,'usuarios': Usuario.objects.all()})

        if contrasena != confirmar_contrasena:
            return render(request, 'crearUsuario.html', {'mensaje': "Las contraseñas no coinciden" , 'usuarios': Usuario.objects.all()})

        usuario = Usuario.objects.create(
            nombre=nombre,
            apellido=apellido,
            email=email,
            contrasena=make_password(contrasena)
        )
        usuario.save()

        messages.success(request, 'Usuario creado correctamente')
        return redirect('../auth')

    return render(request, 'crearUsuario.html')


def panel(request):
    if 'usuario_email' not in request.session:
        messages.error(request, 'Debes iniciar sesión para acceder al panel')
        return redirect('auth')
    return render(request, 'panel.html')