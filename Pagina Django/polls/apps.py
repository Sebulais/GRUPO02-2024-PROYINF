from django.apps import AppConfig

# Notificaciones

class PollsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
    def ready(self):
        import polls.signals