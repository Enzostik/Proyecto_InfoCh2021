from django import forms
from .models import PerfilUsuario

PROVINCIAS=(('Buenos Aires','Buenos Aires'),
            ('Capital Federal','Capital Federal'),
            ('Catamarca','Catamarca'),
            ('Chaco','Chaco'),
            ('Chubut','Chubut'),
            ('Córdoba','Córdoba'),
            ('Corrientes','Corrientes'),
            ('Entre Ríos','Entre Ríos'),
            ('Formosa','Formosa'),
            ('Jujuy','Jujuy'),
            ('La Pampa','La Pampa'),
            ('La Rioja','La Rioja'),
            ('Mendoza','Mendoza'),
            ('Misiones','Misiones'),
            ('Neuquén','Neuquén'),
            ('Río Negro','Río Negro'),
            ('Salta','Salta'),
            ('San Juan','San Juan'),
            ('San Luis','San Luis'),
            ('Santa Cruz','Santa Cruz'),
            ('Santa Fe','Santa Fe'),
            ('Santiago del Estero','Santiago del Estero'),
            ('Tierra del Fuego','Tierra del Fuego'),
            ('Tucumán','Tucumán'),)

class edit_profile(forms.Form):
    nombre=forms.CharField(max_length=50,required=True)
    apellido=forms.CharField(max_length=50,required=True)
    correo=forms.CharField(max_length=100,required=True)
    provincia = forms.ChoiceField(choices=PROVINCIAS, required=True)
    localidad= forms.CharField(max_length=50, required=False)
    visibilidad= forms.BooleanField(label='Visibilidad', required=False)
