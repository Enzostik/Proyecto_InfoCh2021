from .forms import checkTipo
#para los mensajes de error
from django.contrib import messages
from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#cargar los modelos de db
from .models import Pregunta, Respuesta, Partida
from django.db.models import Q #para busqueda de lista de palabras
from functools import reduce #para busqueda de lista de palabras
from datetime import datetime


nombre_clasificaciones={
    'CULTURA':'Cultura y arte',
    'HISTORIA':'Historia',
    'DEPORTE':'Deporte',
    'GEOGRAFIA':'Geografía',
    'ECONOMIA':'Economía',
    'CIENCIA':'Ciencia y Educación',
    'ENTRETENIMIENTO':'Entretenimiento'
}

def ver_partida(request,id):
    try:
        partida=Partida.objects.get(pk=id)
    except:
        raise Http404
    context={'partida':partida}
    return render(request,'juego/partida.html',context)


def generar_cuestionario(cantidad,temas):
    #cargar las preguntas aleatorias
    if temas: #si se definieron temas
        temas=temas.split('!')[0:-1]
        random_preguntas=Pregunta.objects.filter(clasificacion__in=temas).order_by('?')[:cantidad]
    else: #si no se definieron temas
        random_preguntas=Pregunta.objects.order_by('?')[:cantidad]
    #si no hay suficientes preguntas alzar un error
    if len(random_preguntas)<cantidad:
        return "ERROR"
    #cargar las respuestas correspondientes ordenadas aleatoriamente
    lista_respuestas={}
    numero_pregunta=1 #siempre habrá una pregunta como mínimo
    for i in random_preguntas:
        i_respuestas=Respuesta.objects.filter(id_pregunta=i.pk).order_by('?')
        lista_respuestas[i]=[numero_pregunta,i_respuestas,nombre_clasificaciones[i.clasificacion]]
        numero_pregunta+=1
    return lista_respuestas

@login_required(login_url="login")
def jugar(request,cant=0,temas=0):
    #si la request es el POST de un formulario
    #analizar la respuesta a la partida
    if request.method == "POST":
        formulario_usuario=request.POST.getlist("formularioUsuario")
        respuestas_partida=[request.POST.getlist(f"RadioRespuesta_{i}") for i in formulario_usuario]
        puntaje_partida=0

        for i in respuestas_partida:
            i_respuesta=Respuesta.objects.get(pk=i[0])
            puntaje_partida+=i_respuesta.es_correcta #si es True=1 ; False=0

        #crear la "Partida" en la base de datos
        partida_nueva=Partida(usuario=request.user,puntuacion=puntaje_partida)
        partida_nueva.save()

        '''PONER UN REDIRECT A LA PAGINA DE RESULTADO PARA COMPARTIRLA'''
        return HttpResponseRedirect(f'/partida/ver/{partida_nueva.pk}')
    #obtiene el nivel de la url
    cant = request.GET.get('level', 0)
    temas = request.GET.get('temas', 0)
    #si no era un POST
    lista_respuestas=generar_cuestionario((5+int(cant)),temas) #generar un cuestionario con 5 preguntas
    if lista_respuestas == "ERROR":
        messages.add_message(request, messages.ERROR, 'No hay suficientes preguntas, pruebe otra configuración.')
        return redirect("/partida/nuevo/") #regresa la direccion con 'next'
    #envia los datos del cuestionario al jugador
    context={"juego":lista_respuestas}
    return render(request,'juego/jugar.html',context)

@login_required(login_url="login")
def nuevo_juego(request):
    form=checkTipo()
    context={"form":form,"is_error":False}
    if request.method=="POST":
        dificultad=request.POST.get("DificultadCuestionario")
        form=checkTipo(request.POST)
        if form.is_valid():
            form=form.clean() #limpiar el contenido para obtener las variables

            #Si no se seleccionaron temas alza un error.
            temas=''
            for i in form:
                if form[i]:
                    temas+=i+'!'
            if not temas:
                messages.add_message(request, messages.ERROR, 'Debe marcar al menos un campo de preguntas.')
                return redirect("/partida/nuevo/") #regresa la direccion con 'next'
            

        return HttpResponseRedirect(f'/partida/jugar/?level={dificultad}&temas={temas}')
    return render(request,'juego/nueva_partida.html',context)

'''def revisar_partida(user,id,cant):
    partidas=Partida.objects.filter(usuario=user).order_by("-fecha")
    #ordenar para pasar a las tablas
    cant_partidas=[]
    for i in range(ceil(len(partidas)/cant)):
        cant_partidas.append(str(i+1))
    partidas=partidas[cant*(id-1):cant*id] #toma de a 20 las partidas para enviar
    tabla_partidas={}
    n_partida=1 #empieza a contar desde la primer partida
    for i in partidas:
        tabla_partidas[n_partida]=i
        n_partida+=1
    return partidas, cant_partidas'''

def buscar_partida(user_obj,ordenar_por,buscar_todos=False):
    if buscar_todos:
        return Partida.objects.all().order_by(f"-{ordenar_por}")
    #devuelve las partidas que se encontraron para el usuario ordanadas por tal parámetro
    return Partida.objects.filter(usuario=user_obj).order_by(f"-{ordenar_por}")

def revisar_partida(partidas,page,cant):
    paginator=Paginator(partidas,cant)
    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)

def buscador(request):
    #armar la url: /?page=&search=&ord=&met=&num=
    #configuracion y variables de búsqueda
    page=request.GET.get('page', 1) #numero de la página de resultados
    buscar = request.GET.get('search', None)
    orden = request.GET.get('ord', 0) #por defecto busca descendente
    metodo = request.GET.get('met', "fecha") #por defecto busca por fecha
    cantidad = request.GET.get('num', 20) #Cantidad por página, 20 por defecto

    orden=["-",""][int(orden)]

    if buscar:#si se define palabras clave las filtra
        buscar=buscar.split("+¡")[0:-1]
        partidas=Partida.objects.filter(reduce(lambda x, y: x | y, [Q(usuario__contains=x) for x in buscar])).order_by(orden+metodo)
    else: #en caso contrario busca todas las partidas en la db
        partidas=Partida.objects.all().order_by(orden+metodo)
    print(orden+metodo)
    resultados_paginados=revisar_partida(partidas,int(page),int(cantidad))

    context={"partidas":resultados_paginados, "ranking":True}
    return render(request, 'juego/buscador_partidas.html',context)