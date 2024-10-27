from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index. SEXOOOOOOOOOOOOOOOOOOO  sexoooo lol, llamenla, ola sebas")

def home(request):
    return render(request, "test.html")

def noticias(request):
    return render(request, "home.html")

def programas(request):
    return HttpResponse("Esto fue un accidente de pancha")

def convocatorias(request):
    return HttpResponse("Inserten meme")

def contacto(request):
    return HttpResponse("AAAAAAAAAAA")