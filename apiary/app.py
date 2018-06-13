from django.apps import AppConfig


class ApiaryConfig(AppConfig):
    name = 'apiary'

    def ready(self):
        import apiary.signals
