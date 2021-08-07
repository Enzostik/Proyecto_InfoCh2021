import uuid #para generar URL unicas
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import User



class Clasificacion(models.TextChoices):
    GEOGRAFIA = 'Geografía'
    HISTORIA = 'Historia'
    POLITICA = 'Politica'
    SOCIAL = 'Social'
    CULTURAL = 'Cultural'

'''class Clasificacion(models.Model):
    tipo=models.CharField(max_lenght=30)'''

class Pregunta(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE) #modificar mas adelante
    pregunta = models.CharField(max_length=500)
    clasificacion = models.CharField(max_length=30,choices=Clasificacion.choices,default=Clasificacion.GEOGRAFIA,)
    fecha_creacion = models.DateTimeField(auto_now_add=True, editable=False)
    fecha_modificacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pregunta

class Respuesta(models.Model):
    id_pregunta=models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    es_correcta=models.BooleanField(default=False)
    respuesta=models.CharField(max_length=500)

    def __str__(self):
        return self.respuesta

class Partida(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario=models.ForeignKey(User,on_delete=models.CASCADE)
    puntuacion=models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)