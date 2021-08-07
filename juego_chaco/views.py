import random
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