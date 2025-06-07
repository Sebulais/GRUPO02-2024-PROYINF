from google.cloud import translate
from django.core.mail import send_mail
from .models import Usuario
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

def traducir_texto(texto, idioma_destino='en'):
    print(texto)
    # Crear cliente de Google Translate
    client = translate.TranslationServiceClient()


    project_id = 'ID_a_conseguir'

 
    location = 'global'
    parent = f'projects/{project_id}/locations/{location}'

    # Realizar la traducción
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [texto],
            "mime_type": "text/plain",  
            "source_language_code": 'en',  
            "target_language_code": idioma_destino  
        }
    )
    print(response.translations[0].translated_text)
    return response.translations[0].translated_text

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