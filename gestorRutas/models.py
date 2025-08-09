from django.db import models

# Create your models here.
class Departamento(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

class Municipio(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    departamento = models.ForeignKey('Departamento', on_delete=models.CASCADE, related_name='municipios')

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(primary_key=True)
    contrasena = models.CharField(max_length=300)

class Ruta(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    fecha = models.DateField()
    descripcion = models.TextField()
    distancia = models.FloatField()
    duracion = models.FloatField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='rutas')

class Recuerdo(models.Model):
    id = models.AutoField(primary_key=True)
    ruta = models.ForeignKey(Ruta, null=True, on_delete=models.CASCADE, related_name='items')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    orden = models.IntegerField(null=True)
    destino = models.ForeignKey(Departamento, null=True, on_delete=models.CASCADE, related_name='recuerdos')

class Destino(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    ruta = models.ForeignKey(Ruta, null=True, on_delete=models.CASCADE, related_name='destinos')
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, related_name='destinos')

class Archivo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    archivo = models.BinaryField()
    tipo = models.CharField(max_length=100)
    ruta = models.ForeignKey(Ruta, null=True, on_delete=models.CASCADE, related_name='archivos')
    recuerdo = models.ForeignKey(Recuerdo, null=True, on_delete=models.CASCADE, related_name='archivos')
    destino = models.ForeignKey(Destino, null=True, on_delete=models.CASCADE, related_name='archivos')