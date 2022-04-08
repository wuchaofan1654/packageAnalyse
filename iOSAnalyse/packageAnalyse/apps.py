from django.apps import AppConfig


class PackagesizeanalyseConfig(AppConfig):
    name = 'packageAnalyse'

    def ready(self):
        pass
        # from .signals import publish_saved_callback
