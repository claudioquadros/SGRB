from django.apps import AppConfig


class InseminationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inseminations'

    def ready(self):
        import inseminations.signals  # noqa
