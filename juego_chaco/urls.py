from django.urls import path
from . import views

urlpatterns = [
    path('nuevo/',views.nuevo_juego,name="nuevo-juego"),
    path('jugar/',views.jugar,name="jugar"),
    path('jugar/?level=<int:cant>',views.jugar,name="jugar"),
    path('ver/<str:id>',views.ver_partida,name="ver-partida"),
]