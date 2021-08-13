#Carga los datos de la db
from juego_chaco.models import Partida, Pregunta, Respuesta
from django.contrib.auth.models import User
from django.http.response import Http404, HttpResponseRedirect

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from datetime import datetime

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
    print(lista_partidas)
    context={"partidas":lista_partidas}
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
    print(pregunta.pk)        
    return HttpResponseRedirect('/editar/ver/%d'%pregunta.pk)

def borrar_pregunta(request, id):
    Pregunta.objects.get(pk=id).delete()
    return HttpResponseRedirect('/useradmin/prg')

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
    sw={"new":crear_pregunta,"del":borrar_pregunta,"ver":ver_pregunta}
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