from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import InformacionCientifica, Boletin
from .utils import notificar

@receiver(post_save, sender=Boletin)
def boletin_listo_notificacion(sender, instance, **kwargs):
    if instance.estado == 'Listo para revisión':
        notificar('boletin_listo', instance)

@receiver(post_save, sender=InformacionCientifica)
def info_relevante_notificacion(sender, instance, created, **kwargs):
    if instance.es_relevante:
        print("Señal activada para enviar correo")
        notificar('nueva_info_relevante', instance)