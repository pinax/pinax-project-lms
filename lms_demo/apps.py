from django.apps import AppConfig as BaseAppConfig
from django.utils.importlib import import_module


class AppConfig(BaseAppConfig):

    name = "lms_demo"

    def ready(self):
        import_module("lms_demo.receivers")
