from django.shortcuts import render

from django.http import HttpResponse

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import google.generativeai as genai
from .utils import traducir_textos
from .utils import synthesize_text
from django.views.decorators.http import require_GET

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import InformacionCientifica
from .serializers import InformacionCientificaSerializer


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

@csrf_exempt
@require_GET  # Exime la verificación de CSRF para facilitar pruebas locales
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

@require_GET
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@require_GET
def get_idioma_navegador(request):
    aceptado = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
    if aceptado:
        return aceptado.split(',')[0][:2]
    return 'en'

@require_GET
def noticias(request):
    return render(request, "home.html")

@require_GET
def boletines(request):
    return render(request, "boletines.html")

@require_GET
def generarBoletines(request):
    return render(request, "generarBoletines.html")

@require_GET
def programas(request):
    return HttpResponse("Esto fue un accidente de pancha")

@require_GET
def convocatorias(request):
    return HttpResponse("Inserten meme")

@require_GET
def contacto(request):
    return render(request, "contacto.html")

@require_GET
def home(request):
    return render(request, "test.html")

@require_GET
def textSpeech(request):
    import random
    import string
    
    if request.method == "POST":
        letters = string.ascii_lowercase

        file_name = f"{''.join(random.choice(letters) for i in range(10))}.mp3"
        dir = os.getcwd()+"/polls/static/sound_file"
        full_dir = dir + "/"+file_name

        text = request.POST['text']
        lang = request.POST['lang']
        
        synthesize_text(full_dir,text,lang)
        data = {"loc" :file_name}
        
        return render(request,'mostrarAudio.html',data)

    return render(request, "textSpeech.html")

@require_GET
def translate(request):
    texto_original = ""
    texto_traducido = ""

    if request.method == "POST":
        texto_original = request.POST.get("texto_a_traducir", "")
        if texto_original.strip():
            traducciones = traducir_textos({"text": texto_original}, idioma_destino="en")
            texto_traducido = traducciones.get("text", "")

    return render(request, "translate.html", {
        "texto_original": texto_original,
        "texto_traducido": texto_traducido,
    })


class CrearInformacionCientifica(APIView):
    def post(self, request):
        print("POST recibido con data:", request.data)
        serializer = InformacionCientificaSerializer(data=request.data)
        if serializer.is_valid():
            print("Serializer válido, guardando...")
            serializer.save()  # Esto debe disparar la señal
            print("Guardado exitoso")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Serializer inválido:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)