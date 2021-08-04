from django.contrib import admin
from .models import Pregunta, Respuesta, Partida

# Register your models here.

@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display=('pregunta','clasificacion','fecha_creacion')

@admin.register(Respuesta)
class RespuestaAdmin(admin.ModelAdmin):
    list_display=('id_pregunta','respuesta','es_correcta')

@admin.register(Partida)
class PartidaAdmin(admin.ModelAdmin):
    list_display=('fecha','usuario','puntuacion')

