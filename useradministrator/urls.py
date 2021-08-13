from django.urls import path
from . import views

urlpatterns = [
    path('useradmin/<str:id>',views.mi_useradmin,name="mi_useradmin"),
    path('editar/<str:operacion>',views.editar_pregunta_admin,name="editar"),
    path('editar/<str:operacion>/<str:id>',views.editar_pregunta_admin,name="editar"),
]
