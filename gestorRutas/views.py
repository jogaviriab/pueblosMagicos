from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from .models import Usuario, Ruta, Archivo, Departamento, Municipio,Destino
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
        archivos = Archivo.objects.filter(ruta__usuario__email=request.session['usuario_email'])



        archivos_context = []
        for archivo in archivos:
            archivos_context.append({
                'nombre': archivo.nombre,
                'ruta_id': archivo.ruta_id,
                'tipo': archivo.tipo,
                'archivo': base64.b64encode(archivo.archivo).decode('utf-8'),  # Esto da solo el string base64
            })

        destinos = Destino.objects.filter(ruta__usuario__email=request.session['usuario_email'])

    return render(request, 'misRutas.html',{'rutas' : rutas, 'archivos': archivos_context,'destinos': destinos})

def crearRuta(request):
    departamentos = Departamento.objects.all()
    municipios = Municipio.objects.all()
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
        estado = request.POST.get('estado')

        ruta = Ruta(
            nombre=nombre,
            estado=estado,
            descripcion=descripcion,
            fecha=fecha,
            distancia=distancia,
            duracion=duracion,
            usuario=Usuario.objects.get(email=request.session['usuario_email']),
        )
        ruta.save()
        #archivos
        cantidad_archivos = request.POST.get('cantidad_archivos')
        for i in range(1,int(cantidad_archivos)+1):
            archivo = request.FILES.get(f'archivo{i}')
            archivo_model = Archivo(
                nombre="archivo-1 "+nombre,
                ruta=ruta,
                archivo=archivo.read(),
                tipo=archivo.content_type,
            )
            archivo_model.save()

        #destinos
        cantidadDestios = request.POST.get('cantidad_destinos')
        for i in range(1,int(cantidadDestios)+1):
            nombreDestino = f'destino{i}'
            descripcionDestino = 'No hay descripcion'
            idMunicipio = request.POST.get(f'municipio{i}')
            municipio = Municipio.objects.get(id=idMunicipio)
            destino = Destino(
                nombre=nombreDestino,
                descripcion=descripcionDestino,
                ruta=ruta,
                municipio=municipio,
            )
            destino.save()

        messages.success(request, 'Ruta creada correctamente')
        return redirect('misRutas')

    return render(request, 'crearRuta.html',{'departamentos': departamentos, 'municipios': municipios})

def verRuta(request, ruta_id):
    if 'usuario_email' not in request.session:
        messages.error(request, 'Debes iniciar sesión para ver la ruta')
        return redirect('login')

    try:
        ruta = Ruta.objects.get(id=ruta_id, usuario__email=request.session['usuario_email'])
        archivos = Archivo.objects.filter(ruta_id=ruta)
        destinos = Destino.objects.filter(ruta_id=ruta)
    except Ruta.DoesNotExist:
        messages.error(request, 'Ruta no encontrada')
        return redirect('misRutas')
    print(f'Cantidad de archivos: {len(archivos)}')
    archivos_context = []
    for archivo in archivos:
        archivos_context.append({
            'nombre': archivo.nombre,
            'tipo': archivo.tipo,
            'archivo': base64.b64encode(archivo.archivo).decode('utf-8'),
        })
    print(f'Cantidad de archivos context: {len(archivos_context)}')
    cantidad=len(archivos_context)

    return render(request, 'verRuta.html', {'ruta': ruta, 'archivos': archivos_context, 'destinos': destinos, 'cantidad': cantidad})