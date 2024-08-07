from django.apps import AppConfig


class ManagementsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "managements"
    verbose_name = "Manage Locations"

    def ready(self):
        import managements.signals