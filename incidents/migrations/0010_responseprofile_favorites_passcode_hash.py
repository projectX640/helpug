from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("incidents", "0009_incident_notes_and_favorites")]

    operations = [
        migrations.AddField(
            model_name="responseprofile",
            name="favorites_passcode_hash",
            field=models.CharField(blank=True, editable=False, max_length=128),
        ),
    ]
