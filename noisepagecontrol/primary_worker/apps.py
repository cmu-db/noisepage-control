from django.apps import AppConfig


class PrimaryWorkerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "primary_worker"
