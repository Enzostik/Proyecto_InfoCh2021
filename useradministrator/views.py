#Carga los datos de la db
from juego_chaco.models import Partida, Pregunta, Respuesta
from django.contrib.auth.models import User
from django.http.response import Http404, HttpResponseRedirect

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from datetime import datetime, date, timedelta

#Paginas solo para administradores:

def admin_usuarios(request):
    lista_usuarios={}
    u=User.objects.all()
    for i in u:
        if i.has_perm('authusuario.es_usuario_admin'):
            lista_usuarios[i]=True
        else:
            lista_usuarios[i]=False
    context={"users":lista_usuarios}
    return render(request,'admin/admin_usuarios.html',context)

def admin_actividades(request):
    lista_partidas=Partida.objects.all()
    #armar un diccionario para las estadísticas generales
    fecha_hoy=date.today()
    partidas_hoy=lista_partidas.filter(fecha__contains=fecha_hoy)
    partidas_semana=lista_partidas.filter(fecha__week=fecha_hoy.isocalendar().week)
    partidas_mes=lista_partidas.filter(fecha__contains=fecha_hoy.month)
    estadisticas={
        "total":len(lista_partidas),
        "mejor":lista_partidas.order_by('-puntuacion').first(),
        "diario":len(partidas_hoy),
        "mejor_diario":partidas_hoy.order_by('-puntuacion').first(),
        "semanal":len(partidas_semana),
        "mejor_semanal":partidas_semana.order_by('-puntuacion').first(),
        "mensual":len(partidas_mes),
        "mejor_mes":partidas_mes.order_by('-puntuacion').first(),
    }
    context={"partidas":lista_partidas,"estadisticas":estadisticas}
    return render(request,'admin/admin_actividades.html',context)

def admin_cuestionarios(request):
    lista_preguntas=Pregunta.objects.all()
    context={"cuestionario":lista_preguntas}
    return render(request,'admin/admin_cuestionarios.html',context)

def crear_pregunta(request,id):
    pregunta=Pregunta(autor=request.user,pregunta="Nueva pregunta")
    pregunta.save()
    for i in range(5):
        respuesta=Respuesta(id_pregunta=pregunta,es_correcta=False,respuesta="Nueva respuesta")
        respuesta.save() 
    return HttpResponseRedirect('/editar/ver/%d'%pregunta.pk)

def borrar_pregunta(request, id):
    Pregunta.objects.get(pk=id).delete()
    return HttpResponseRedirect('/useradmin/prg')

def borrar_respuesta(request,id):
    rta=Respuesta.objects.get(pk=id)
    id_preg=rta.id_pregunta.pk
    rta.delete()
    return HttpResponseRedirect(f'/editar/ver/{id_preg}')

def nueva_respuesta(request,id):
    preg=Pregunta.objects.get(pk=id)
    rta=Respuesta(id_pregunta=preg,respuesta="Nueva Respuesta")
    rta.save()
    return HttpResponseRedirect(f'/editar/ver/{preg.pk}')

def ver_pregunta(request,id):
    try:
        pregunta=Pregunta.objects.get(pk=id)
        respuestas=Respuesta.objects.filter(id_pregunta=pregunta)
    except:
        raise Http404
    if request.POST:
        cont_pregunta=request.POST.get('pregunta')
        clasif_pregunta=request.POST.get('preguntaSelect')
        cont_respuesta=request.POST.getlist('respuesta')
        bool_respuesta = [request.POST.get(f'respuestaBool_{i.pk}') == 'Verdadero' for i in respuestas]

        #cambiar el contenido de la pregunta
        pregunta.pregunta=cont_pregunta
        pregunta.clasificacion=clasif_pregunta
        pregunta.fecha_modificacion=datetime.now()
        pregunta.save()

        recorrido=0
        for i in respuestas:
            #cambiar el contenido de la respuesta
            i.respuesta=cont_respuesta[recorrido]
            i.es_correcta=bool_respuesta[recorrido]
            i.save()
            recorrido+=1
        return HttpResponseRedirect('/useradmin/prg')
    context={"pregunta":pregunta,"respuestas":respuestas}
    return render(request, 'admin/editar_preguntas.html',context)

def editar_pregunta(request,operacion,id):
    sw={"new":crear_pregunta,"del":borrar_pregunta,"ver":ver_pregunta,"newr":nueva_respuesta,"delr":borrar_respuesta}
    func= sw.get(operacion,"ERROR")
    if func != "ERROR":
        return func(request,id)
    raise Http404

#Funcion principal que verifica los permisos de los usuarios
@login_required(login_url="login")
@permission_required('authusuario.es_usuario_admin',raise_exception=True)
def mi_useradmin(request,id):
    sw={"prg":admin_cuestionarios,"usr":admin_usuarios,"act":admin_actividades}
    func= sw.get(id,"ERROR")
    if func != "ERROR":
        return func(request)
    raise Http404

@login_required(login_url="login")
@permission_required('authusuario.es_usuario_admin',raise_exception=True)
def editar_pregunta_admin(request,operacion,id=1):
    return editar_pregunta(request,operacion,id)