from django.shortcuts import render

from django.http import HttpResponse

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import google.generativeai as genai
from .utils import traducir_texto

def home(request):
    contenido = {
        'titulo': 'Bienvenido a la biblioteca local',
        'noticias': [
            'El servidor fue actualizado exitosamente.',
            'Nuevas características han sido añadidas.',
        ]
    }

    idioma_navegador = request.LANGUAGE_CODE

    if idioma_navegador != 'es':
        contenido['titulo'] = traducir_texto(contenido['titulo'], idioma_destino=idioma_navegador)
        contenido['noticias'] = [traducir_texto(nota, idioma_destino=idioma_navegador) for nota in contenido['noticias']]

    return render(request, 'home.html', {'contenido': contenido})

# Configurar la API de Google Generative AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="You'll speak in Spanish from now on. You're a specialist AI that helps in the FIA Chile.",
)

history = []  # Historial de la conversación

@csrf_exempt  # Exime la verificación de CSRF para facilitar pruebas locales
def chat_view(request):
    if request.method == "POST":
        try:
            # Extraer mensaje del cliente
            body = json.loads(request.body)
            user_input = body.get("message", "").strip()
            if not user_input:
                return JsonResponse({"error": "El mensaje no puede estar vacío."}, status=400)

            # Crear sesión de chat con el historial
            chat_session = model.start_chat(history=history)
            response = chat_session.send_message(user_input)
            model_response = response.text

            # Actualizar el historial
            history.append({"role": "user", "parts": [user_input]})
            history.append({"role": "system", "parts": [model_response]})

            return JsonResponse({"reply": model_response})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Método no permitido."}, status=405)



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