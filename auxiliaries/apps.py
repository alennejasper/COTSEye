from django.apps import AppConfig


class AuxiliariesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "auxiliaries"
    verbose_name = "Others"

    def ready(self):
        import auxiliaries.signals