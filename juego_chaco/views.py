import random
from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required

#cargar los modelos de db
from .models import Pregunta, Respuesta, Partida

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

def editar_pregunta(request,id):
    if id=="new":
        new_id=crear_pregunta(request,5) #crear una nueva pregunta con 5 respuestas vacias
        return HttpResponseRedirect('/editar/%d'%new_id)
    try:
        pregunta=Pregunta.objects.get(pk=id)
        respuestas=Respuesta.objects.filter(id_pregunta=pregunta)
    except:
        raise Http404
    if request.POST:
        cont_pregunta=request.POST.get('pregunta')
        cont_respuesta=request.POST.getlist('respuesta')
        print(cont_pregunta)
        pregunta.pregunta=cont_pregunta
        pregunta.save()
        recorrido=0
        for i in respuestas:
            i.respuesta=cont_respuesta[recorrido]
            i.save()
            recorrido+=1
        return HttpResponseRedirect('/useradmin/prg')
    context={"pregunta":pregunta,"respuestas":respuestas}
    return render(request, 'admin/editar_preguntas.html',context)