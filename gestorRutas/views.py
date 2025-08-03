from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from .models import Usuario, Ruta, Archivo
import base64
from datetime import datetime


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
        return redirect('auth')

    return render(request, 'crearUsuario.html')


def panel(request):
    if 'usuario_email' not in request.session:
        messages.error(request, 'Debes iniciar sesión para acceder al panel')
        return redirect('login')
    return render(request, 'panel.html')

def misRutas(request):
    if 'usuario_email' not in request.session:
        messages.error(request, 'Debes iniciar sesión para ver tus rutas')
        return redirect('login')
    else:
        rutas = Ruta.objects.filter(usuario__email=request.session['usuario_email'])
    return render(request, 'misRutas.html',{'rutas' : rutas})

def crearRuta(request):
    if 'usuario_email' not in request.session:
        messages.error(request, 'Debes iniciar sesión para crear una ruta')
        return redirect('login')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        fecha_str = request.POST.get('fecha')
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        distancia = request.POST.get('distancia')
        duracion = request.POST.get('duracion')

        print("IMprimiendo datos de la ruta")
        print(nombre, descripcion, fecha, distancia, duracion)

        ruta = Ruta(
            nombre=nombre,
            estado='En curso',
            descripcion=descripcion,
            fecha=fecha,
            distancia=distancia,
            duracion=duracion,
            usuario=Usuario.objects.get(email=request.session['usuario_email']),
        )
        ruta.save()
        #archivos
        cantidad_archivos = request.POST.get('cantidad_archivos')
        print(cantidad_archivos)
        for i in range(1,int(cantidad_archivos)+1):
            print(i)
            print(f'archivo{i}')
            archivo = request.FILES.get(f'archivo{i}')
            archivo_b64 = base64.b64encode(archivo.read())
            archivo_model = Archivo(
                nombre="archivo-1 "+nombre,
                ruta=ruta,
                archivo=archivo_b64,
            )
            archivo_model.save()
        messages.success(request, 'Ruta creada correctamente')
        return redirect('misRutas')

    return render(request, 'crearRuta.html')