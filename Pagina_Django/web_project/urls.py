"""
URL configuration for web_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from polls.views import home, index, boletines, noticias, programas, convocatorias, contacto, generarBoletines, chat_view, textSpeech, translate, CrearInformacionCientifica
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home, name='home'),
    path('index/', index, name='index'),
    path('boletines/', boletines, name='boletines'),
    path('noticias/', noticias, name='noticias'),
    path('programas/', programas, name='programas'),
    path('convocatorias/', convocatorias, name='convactorias'),
    path('contacto/', contacto, name='contacto'),
    path('generarBoletines/', generarBoletines, name='generarBoletines'),
    path('api/chat/', chat_view, name='chat_view'),
    path('textSpeech/', textSpeech, name='textSpeech'),
    path("translate/", translate, name="translate"),
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
    path("i18n/", include("django.conf.urls.i18n")),
    path("api/informacion-cientifica/", CrearInformacionCientifica.as_view(), name="informacion"),
    
]
