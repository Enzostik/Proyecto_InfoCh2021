from django.db import models

class Permisos(models.Model):
    class Meta:
        permissions = [
            ("es_usuario_admin", "Acceso a herramientas del sitio"),
            ("es_super_admin","Acceso total al sitio")
        ]