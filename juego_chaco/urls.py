from django.urls import path
from . import views

urlpatterns = [
    path('jugar/',views.jugar,name="jugar"),
]