from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'index.html') #ejemplo para pagina principal

def page_not_found(request,exception):
    return render(request,'page404.html')