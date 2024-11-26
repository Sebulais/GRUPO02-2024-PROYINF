from django.urls import path, include
from django.contrib import admin
from django.conf.urls.static import static
from . import views
from django.urls import path
from .views import chat_ia
urlpatterns = [
    path("api/chat/", views.chat_ia, name="chat_ia"),
    path("contacto/", chat_ia, name="contacto"),
    path("", chat_ia, name="chat_ia"),  # URL para las peticiones AJAX
    path("", views.index, name="index"),
    path("", views.home, name="home"),
    path("", views.boletines, name="boletines"),
    path("", views.noticias, name="noticias"),
    path("",views.programas, name= "programas"),
    path("", views.convocatorias, name="convocatorias"),
    path("", views.contacto, name="contacto"),
    path("", views.generarBoletines, name="generarBoletines"),
]

