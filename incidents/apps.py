from django.apps import AppConfig
from django.db.backends.signals import connection_created


def configure_sqlite(connection, **kwargs):
    if connection.vendor != "sqlite":
        return
    with connection.cursor() as cursor:
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute("PRAGMA busy_timeout = 20000")
        cursor.execute("PRAGMA journal_mode = WAL")
        cursor.execute("PRAGMA synchronous = NORMAL")
        cursor.execute("PRAGMA wal_autocheckpoint = 1000")


class IncidentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "incidents"

    def ready(self):
        connection_created.connect(configure_sqlite, dispatch_uid="incidents.configure_sqlite")
