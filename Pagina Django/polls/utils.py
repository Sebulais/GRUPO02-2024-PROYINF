from google.cloud import translate

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