from importlib import import_module

from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):

    name = "miSitio"

    def ready(self):
        import_module("miSitio.receivers")
