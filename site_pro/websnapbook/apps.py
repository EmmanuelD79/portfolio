from django.apps import AppConfig


class WebsnapbookConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'websnapbook'

    def ready(self):
        import websnapbook.signals
