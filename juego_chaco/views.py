import random
from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required

#cargar los modelos de db
from .models import Pregunta, Respuesta, Partida

from datetime import datetime

@login_required(login_url="login")
def jugar(request):
    lista_preguntas=Pregunta.objects.all()
    lista_preguntas=list(lista_preguntas)
    random_preguntas=random.sample(lista_preguntas,5)
    lista_respuestas={}
    for i in random_preguntas:
        lista_respuestas[i]=Respuesta.objects.filter(id_pregunta=i.pk)

    context={"juego":lista_respuestas}
    return render(request,'juego/jugar.html',context)


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