from google.cloud import translate
from django.core.mail import send_mail
from .models import Usuario

def traducir_texto(texto, idioma_destino='en'):
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
            "source_language_code": 'es',  
            "target_language_code": idioma_destino  
        }
    )


    return response.translations[0].translated_text


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
            'noreply@tuapp.com',
            [usuario.email],
            fail_silently=False,
        )