from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def home(request):
    return render(request, "test.html")

def noticias(request):
    return render(request, "home.html")

def boletines(request):
    return render(request, "boletines.html")

def generarBoletines(request):
    return render(request, "generarBoletines.html")

def programas(request):
    return HttpResponse("Esto fue un accidente de pancha")

def convocatorias(request):
    return HttpResponse("Inserten meme")

def contacto(request):
    return render(request, "contacto.html")