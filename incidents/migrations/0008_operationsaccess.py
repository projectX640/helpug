from django.db import migrations, models


def create_operations_access(apps, schema_editor):
    OperationsAccess = apps.get_model("incidents", "OperationsAccess")
    OperationsAccess.objects.get_or_create(pk=1, defaults={"label": "Operations Center"})


class Migration(migrations.Migration):
    dependencies = [("incidents", "0007_emergencyrequest_idempotency_key")]

    operations = [
        migrations.CreateModel(
            name="OperationsAccess",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("label", models.CharField(default="Operations Center", max_length=120)),
                ("passcode_hash", models.CharField(blank=True, editable=False, max_length=128)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RunPython(create_operations_access, migrations.RunPython.noop),
    ]
