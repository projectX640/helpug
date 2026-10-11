from django.db import migrations, models


def rename_legacy_similarity_signal(apps, schema_editor):
    Incident = apps.get_model("incidents", "Incident")
    Incident.objects.filter(similarity_signal="client_uuid_phone").update(similarity_signal="client_uuid")


class Migration(migrations.Migration):
    dependencies = [
        ("incidents", "0035_incident_similarity"),
    ]

    operations = [
        migrations.RunPython(rename_legacy_similarity_signal, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="incident",
            name="similarity_signal",
            field=models.CharField(
                blank=True,
                choices=[("client_uuid", "Client device token")],
                max_length=40,
            ),
        ),
    ]
