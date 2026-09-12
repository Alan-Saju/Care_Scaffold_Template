from django.apps import AppConfig

PLUGIN_NAME = "care_connect"


class CareConnectConfig(AppConfig):
    name = PLUGIN_NAME
    verbose_name = "Care Connect"

    def ready(self):
        from care_connect import signals  # noqa: F401
