from django.apps import AppConfig

class CryptPixConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cryptpix'

    def ready(self):
        import cryptpix.signals