from google.cloud import texttospeech
from google.cloud import translate_v3 as translate
from django.core.mail import send_mail
from .models import Usuario
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import os


def traducir_textos(textos_dict, idioma_destino='en'):
    client = translate.TranslationServiceClient()
    project_id = "traductor-458002"
    location = 'global'
    parent = f'projects/{project_id}/locations/{location}'

    textos_originales = list(textos_dict.values())

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": textos_originales,
            "mime_type": "text/plain",
            "source_language_code": "es",
            "target_language_code": idioma_destino,
        }
    )

    traducciones = response.translations

    resultado = {}
    for clave, traduccion in zip(textos_dict.keys(), traducciones):
        resultado[clave] = traduccion.translated_text

    return resultado



#Logica de Correo
def notificar(evento, objeto):
    if evento == 'nueva_info_relevante':
        asunto = "Nueva información científica relevante"
        mensaje = f"Se ha registrado nueva información relevante: {objeto.titulo}"
        usuarios = Usuario.objects.filter(rol__in=['coordinadora', 'editor'])

    elif evento == 'boletin_listo':
        asunto = "Boletín listo para revisión"
        mensaje = f"El boletín '{objeto.titulo}' está listo para revisión."
        usuarios = Usuario.objects.filter(rol='coordinadora')

    for usuario in usuarios:
        send_mail(
            asunto,
            mensaje,
            'noreply@Django.com',
            [usuario.email],
            fail_silently=False,
        )


def evento(titulo, descripcion, fecha_inicio=None, duracion_min=60):
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    SERVICE_ACCOUNT_FILE = 'polls/traductor-458002-bd8da2aad69d.json'
    CALENDAR_ID = 'sebastianfabu@gmail.com'

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('calendar', 'v3', credentials=credentials)

    if fecha_inicio is None:
        fecha_inicio = datetime.utcnow()

    fecha_fin = fecha_inicio + timedelta(minutes=duracion_min)

    evento = {
        'summary': titulo,
        'description': descripcion,
        'start': {
            'dateTime': fecha_inicio.isoformat() + 'Z',
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': fecha_fin.isoformat() + 'Z',
            'timeZone': 'UTC',
        },
    }

    event = service.events().insert(calendarId=CALENDAR_ID, body=evento).execute()
    print(f"Evento creado: {event.get('htmlLink')}")
    

def synthesize_text(dir, text,language_code='en-US'):
    '''
    pip install --upgrade google-cloud-texttospeech
    instalar gcloud
    gcloud init
    
    '''
    
    
    """Synthesizes speech from the input string of text."""
    credential_path = "polls/traductor-458002-bd8da2aad69d.json"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()
    
    # Set the text input to be synthesized
    input_text = texttospeech.SynthesisInput(text=text)
    
    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )
    
    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    
    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=input_text,
        voice=voice,
        audio_config=audio_config,
    )
    
    # The response's audio_content is binary.
    with open(dir, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)

