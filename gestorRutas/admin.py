from django.contrib import admin

# Register your models here.
from gestorRutas.models import Departamento, Municipio, Usuario, Ruta, Recuerdo, Destino, Archivo

admin.site.register(Departamento)
admin.site.register(Municipio)
admin.site.register(Usuario)
admin.site.register(Ruta)
admin.site.register(Recuerdo)
admin.site.register(Destino)
admin.site.register(Archivo)