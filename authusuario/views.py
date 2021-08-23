from django.forms.forms import Form
from .models import PerfilUsuario
from .forms import edit_profile
from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect

#para los mensajes de error
from django.contrib import messages
#para crear y editar usuarios
from django.core.validators import validate_email
from django.utils.http import is_safe_url
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User


def mi_redirect(request,next): #funcion para verificar si la redireccion es segura, o en caso contrario ir a 'home'
    if next and is_safe_url(url=next, allowed_hosts={request.get_host()},
            require_https=request.is_secure()):
        return redirect(next) #si es pagina segura regresa la redireccion
    return redirect('home') #si no es segura o no hay next --> ir a la pag principal 'home'

def mi_check_user(usuario_soy,usuario_obj):
    return (usuario_soy.has_perm('authusuario.es_usuario_admin') or usuario_obj.perfilusuario.visibilidad_perfil or usuario_soy==usuario_obj)

# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=="POST":
        valuenext= request.POST.get('next') #para saber la siguiente url

        context={'is_error':False, 'data':request.POST, 'valuenext':valuenext}
        username=request.POST.get('username').lower()
        password=request.POST.get('password')
        remember_me=request.POST.get('remember-me',False)
        
        if User.objects.filter(username=username).exists():
            user = authenticate(username=username, password=password)
            if user is not None:
                do_login(request, user)
                if not remember_me: #si la check-box no esta marcada ejecuta
                    request.session.set_expiry(0) #la sesion finaliza al cerrar el navegador
                return mi_redirect(request, valuenext) #si detecta el valor /next/ para ir a otra pagina despues de logearse

            else:
                context['is_error']=True
        else:
            context['is_error']=True

        if context['is_error']:
            messages.add_message(request, messages.ERROR, 'Usuario o contraseña incorrecta.')
            return redirect("/login/"+"?next="+valuenext) #regresa la direccion con 'next'
    return render(request,'user/login.html')

def logout(request):
    if request.user.is_authenticated:
        do_logout(request)
    return redirect('home')

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=="POST":
        context={'is_error':False, 'data':request.POST}
        username = request.POST.get('username').lower()
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if not username or not password or not email or not password2:
            messages.add_message(request, messages.ERROR, 'Complete todos los campos requeridos')
            context['is_error']=True

        if len(username)<8:
            messages.add_message(request, messages.ERROR, 'El nombre de usuario debe tener más de 8 carácteres')
            context['is_error']=True

        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR, 'El nombre de usuario ya está tomado')
            context['is_error']=True

        if email:
            try:
                validate_email(email)
            except:
                messages.add_message(request, messages.ERROR, 'Ingrese un correo electrónico válido')
                context['is_error']=True

        if User.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR, 'El correo electrónico ya está registrado')
            context['is_error']=True

        if len(password)<8:
            messages.add_message(request, messages.ERROR, 'La contraseña debe tener más de 8 carácteres')
            context['is_error']=True

        if password!=password2:
            messages.add_message(request, messages.ERROR, 'La contraseña no coincide')
            context['is_error']=True

        if context['is_error']:
            return render(request,'user/register.html',context) #si hay error devuelve a la pagina 'register' pero con los campos guardados

        user=User.objects.create_user(username=username,email=email,password=password)
        profile=PerfilUsuario(usuario=user)
        profile.save()
        return redirect('login')

    return render(request,'user/register.html')

#para la pagina de usuario
@login_required(login_url="login")
def profile(request):
    form=edit_profile()
    context={"form":form,"is_error":False} #asigna un nombre a la base de datos
    if request.method=="POST":
        form=edit_profile(request.POST)
        print(form)
        if form.is_valid():
            form=form.clean()
            print(form)

            #para revisar los errores
            if not form['nombre'] or not form['apellido'] or not form['provincia'] or not form['correo']:
                messages.add_message(request, messages.ERROR, 'Complete todos los campos requeridos')
                context['is_error']=True
            
            if form['correo']:
                try:
                    validate_email(form['correo'])
                except:
                    messages.add_message(request, messages.ERROR, 'Ingrese un correo electrónico válido')
                    context['is_error']=True

            if User.objects.filter(email=form['correo']).exists() and request.user.email != form['correo']:
                messages.add_message(request, messages.ERROR, 'El correo electrónico ya está registrado')
                context['is_error']=True

            if context['is_error']:
                return render(request,'user/profile.html',context) #si hay error devuelve a la pagina 'register' pero con los campos guardados
            #cambiar la base de datos (actualizar el usuario y su perfil)
            print(form)
            usuario=request.user
            usuario.first_name=form["nombre"]
            usuario.last_name=form["apellido"]
            usuario.email=form["correo"]            
            perfil=PerfilUsuario.objects.get(usuario=usuario)
            perfil.provincia=form["provincia"]
            perfil.localidad=form["localidad"]
            perfil.image=form['image']
            perfil.visibilidad_perfil=form["visibilidad"]    
            usuario.save()              
            perfil.save()

    return render(request,'user/profile.html',context)

def ver_usuario(request,id):
    usuario_obj=User.objects.get(pk=id)
    usuario_soy=request.user
    #Verifica si el se tienen parmisos admin | si la cuenta es publica | si es la cuenta del usuario
    datos = mi_check_user(usuario_soy,usuario_obj)
    context={"usuario":usuario_obj,"visibilidad":datos}
    return render(request, 'user/user.html',context)