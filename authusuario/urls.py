from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login,name="login"),
    path('logout',views.logout,name="logout"),
    path('register/',views.register,name="register"),
    path('profile/',views.profile,name="profile"),
    path('user/<int:id>',views.ver_usuario,name="ver_user"),
    path('useradmin/<str:id>',views.mi_useradmin,name="mi_useradmin"),
    path('editar/<str:operacion>',views.editar_pregunta_admin,name="editar"), #si se usa la opcion para crear una nueva pregunta
    path('editar/<str:operacion>/<str:id>',views.editar_pregunta_admin,name="editar"), #si se usa la opcion para ver una pregunta
]
