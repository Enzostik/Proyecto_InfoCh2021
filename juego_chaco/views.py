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

    '''print("Todos los elementos de la base de datos 'Preguntas'")
    for i in lista_preguntas:
        print(i.pk,i.pregunta,i.clasificacion)
    
    print("Seleccion aleatoria de preguntas:")'''

    random_preguntas=random.sample(lista_preguntas,5)

    '''for i in random_preguntas:
        print(i.pk,i.pregunta,i.clasificacion)'''

    '''print("Buscar las respuestas asignadas a la id de la pregunta")'''

    lista_respuestas={}
    for i in random_preguntas:
        respuestas_i=Respuesta.objects.filter(id_pregunta=i.pk)
        lista_respuestas[i]=respuestas_i
        
    '''print("\n\n",lista_respuestas)'''

    context={"juego":lista_respuestas}
    return render(request,'juego/jugar.html',context)


def admin_cuestionarios(request):
    lista_preguntas={}
    p=Pregunta.objects.all()
    for i in p:
        rtas=Respuesta.objects.filter(id_pregunta=i)
        lista_preguntas[i]=len(rtas)
    context={"cuestionario":lista_preguntas}
    return render(request,'admin/admin_cuestionarios.html',context)

def crear_pregunta(request, cant):
    pregunta=Pregunta(autor=request.user,pregunta="Nueva pregunta")
    pregunta.save()
    for i in range(cant):
        respuesta=Respuesta(id_pregunta=pregunta,es_correcta=False,respuesta="Nueva respuesta")
        respuesta.save()
    print(pregunta.pk)        
    return pregunta.pk

def borrar_pregunta(request, id):
    pregunta=Pregunta.objects.get(pk=id)
    pregunta.delete()
    return HttpResponseRedirect('/useradmin/prg')

def editar_pregunta(request,operacion,id):
    if operacion=="new":
        new_id=crear_pregunta(request,5) #crear una nueva pregunta con 5 respuestas vacias
        return HttpResponseRedirect('/editar/ver/%d'%new_id)
    elif operacion=="del":
        return borrar_pregunta(request,id)
    elif operacion=="ver":
        try:
            pregunta=Pregunta.objects.get(pk=id)
            respuestas=Respuesta.objects.filter(id_pregunta=pregunta)
        except:
            raise Http404
        if request.POST:
            cont_pregunta=request.POST.get('pregunta')
            cont_respuesta=request.POST.getlist('respuesta')
            bool_respuesta=request.POST.getlist('respuesta_bool')

            #cambiar el contenido de la pregunta
            pregunta.pregunta=cont_pregunta
            pregunta.fecha_modificacion=datetime.now()
            pregunta.save()

            recorrido=0
            for i in respuestas:
                #cambiar el contenido de la respuesta
                i.respuesta=cont_respuesta[recorrido]
                '''if bool_respuesta[recorrido]:
                    i.es_correcta=True'''
                i.save()
                recorrido+=1
            print(bool_respuesta)
            return HttpResponseRedirect('/useradmin/prg')
        context={"pregunta":pregunta,"respuestas":respuestas}
        return render(request, 'admin/editar_preguntas.html',context)
    else:
        raise Http404