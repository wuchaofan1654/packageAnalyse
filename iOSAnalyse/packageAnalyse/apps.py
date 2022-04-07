from django.apps import AppConfig


class PackagesizeanalyseConfig(AppConfig):
    name = 'packageAnalyse'

    def ready(self):
        from .signals import publish_pre_init_callback
        from .signals import publish_pre_save_callback
        from .signals import publish_saved_callback
