from django import forms
from .models import Clasificacion

class checkTipo(forms.Form):
    CULTURA= forms.BooleanField(label='Cultura y arte', required=False, initial=True)
    HISTORIA = forms.BooleanField(label='Historia', required=False, initial=True)
    DEPORTE = forms.BooleanField(label='Deporte', required=False, initial=True)
    GEOGRAFIA = forms.BooleanField(label='Geografía', required=False, initial=True)
    ECONOMIA = forms.BooleanField(label='Economía', required=False, initial=True)
    CIENCIA = forms.BooleanField(label='Ciencia y Educación', required=False, initial=True)
    ENTRETENIMIENTO = forms.BooleanField(label='Entretenimiento', required=False, initial=True)