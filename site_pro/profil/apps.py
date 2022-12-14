from django.apps import AppConfig


class ProfilConfig(AppConfig):
    name = 'profil'

    def ready(self):
        import profil.signals