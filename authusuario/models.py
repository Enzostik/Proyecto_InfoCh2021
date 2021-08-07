from django.db import models
from django.contrib.auth.models import User

class Permisos(models.Model):
    class Meta:
        permissions = [
            ("es_usuario_admin", "Acceso a herramientas del sitio"),
            ("es_super_admin","Acceso total al sitio")
        ]

class PerfilUsuario(models.Model):
    usuario=models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    visibilidad_perfil=models.BooleanField(default=False) #False - Privado / True - Publico
    descripcion=models.CharField(max_length=500)