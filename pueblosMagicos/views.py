from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from gestorRutas.models import Usuario


def index(request):
    return render(request, 'index.html')
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        contrasena = request.POST.get('contrasena')
        mensaje = 'Usuario '+email+' contraseña '+contrasena
        try:
            usuario = Usuario.objects.get(email=email)
            if check_password(contrasena, usuario.contrasena):
                request.session['usuario_email'] = usuario.email
                return redirect('panel')
            else:
                mensaje = 'correo o contraseña incorrectos'
        except:
            mensaje = 'correo o contraseña incorrectos'
        return render(request, 'login.html', {'mensaje': mensaje})
    return render(request, 'login.html')

def logout(request):
    if 'usuario_email' in request.session:
        del request.session['usuario_email']
    return redirect('index')