# Generated by Django 3.2.6 on 2021-08-19 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authusuario', '0003_alter_perfilusuario_descripcion'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfilusuario',
            name='localidad',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='perfilusuario',
            name='provincia',
            field=models.CharField(default='', max_length=50),
        ),
    ]