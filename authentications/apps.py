from django.apps import AppConfig


class AuthenticationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "authentications"
    verbose_name = "Manage Accounts"

    def ready(self):
        import authentications.signals