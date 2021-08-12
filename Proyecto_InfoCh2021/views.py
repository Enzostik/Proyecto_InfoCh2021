from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'index.html') #ejemplo para pagina principal

def about_us(request):
    return render(request,'about_us.html') #ejemplo para pagina principal

def page_not_found(request,exception):
    context={"titulo":"Página no encontrada", "encabezado": "ERROR 404",
                "contenido": "Página no encontrada. Error 404."}
    return render(request,'page_error.html',context)

def page_not_perm(request,exception):
    context={"titulo":"Acceso no permitido", "encabezado": "PERMISO DENEGADO - ERROR 403",
                "contenido": "No posees los permisos necesarios para ingresar a esta página. Error 403."}
    return render(request,'page_error.html',context)

def page_error_server(request,*args, **argv):
    context={"titulo":"Error", "encabezado": "ERROR 500",
                "contenido": "Ha ocurrido un problema con el servidor."}
    return render(request,'page_error.html',context)