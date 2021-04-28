from django.apps import AppConfig

class GamefiConfig(AppConfig):
    name = 'gamifi'

    def ready(self):
        import gamifi.signals
