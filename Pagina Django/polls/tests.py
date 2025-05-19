import json
from django.test import TestCase
from django.test import TestCase, Client
from django.urls import reverse
from .models import Boletin
# Create your tests here.

class APITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.boletin = Boletin.objects.create(titulo="Boletín 1", estado="Borrador")

# informarcion revelante true,
# Ejecutar casos pruebas en la terminal con este comando: python manage.py test.

