from django.urls import path, include
from django.contrib import admin
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("", views.home, name="home"),
    path("", views.noticias, name="noticias"),
    path("",views.programas, name= "programas"),
    path("", views.convocatorias, name="convocatorias"),
    path("", views.contacto, name="contacto"),
]

