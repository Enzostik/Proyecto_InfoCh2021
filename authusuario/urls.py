from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login,name="login"),
    path('logout',views.logout,name="logout"),
    path('register/',views.register,name="register"),
    path('profile/',views.profile,name="profile"),
    path('useradmin/<str:id>',views.mi_useradmin,name="mi_useradmin"),
]
