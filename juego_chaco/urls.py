from django.urls import path
from . import views

urlpatterns = [
    path('jugar/',views.jugar,name="jugar"),
    path('ver/<str:id>',views.ver_partida,name="ver-partida"),
]