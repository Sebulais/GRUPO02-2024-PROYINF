from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

# Correo para el usuario
class Usuario(models.Model):
    email = models.EmailField()
    rol = models.CharField(max_length=50)  # Ej: 'coordinadora', 'editor'

    def __str__(self):
        return f"{self.email} ({self.rol})"


class InformacionCientifica(models.Model):
    titulo = models.CharField(max_length=255)
    contenido = models.TextField()
    es_relevante = models.BooleanField(default=False)
    def __str__(self):
        return self.titulo

class Boletin(models.Model):
    titulo = models.CharField(max_length=255)
    estado = models.CharField(max_length=50)  # Ej: 'Borrador', 'Listo para revisión'