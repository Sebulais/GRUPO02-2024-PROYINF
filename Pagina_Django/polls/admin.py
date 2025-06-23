from django.contrib import admin
from .models import Boletin

# Register your models here.
from .models import InformacionCientifica

@admin.register(InformacionCientifica)
class InformacionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'es_relevante')

@admin.register(Boletin)
class BoletinAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'estado')