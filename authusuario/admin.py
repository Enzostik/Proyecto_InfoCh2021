from django.contrib import admin
from .models import PerfilUsuario

@admin.register(PerfilUsuario)
class PreguntaAdmin(admin.ModelAdmin):
    list_display=('usuario','visibilidad_perfil')
