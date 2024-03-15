from django.apps import AppConfig


class AppDatabaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_database'

    def ready(self):
        import app_database.signals