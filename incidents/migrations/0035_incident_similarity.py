from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("incidents", "0034_critical_location_tracking"),
    ]

    operations = [
        migrations.AddField(
            model_name="incident",
            name="similar_to",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="repeat_incidents",
                to="incidents.incident",
            ),
        ),
        migrations.AddField(
            model_name="incident",
            name="similarity_checked_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="incident",
            name="similarity_signal",
            field=models.CharField(
                blank=True,
                choices=[
                    ("client_uuid", "Client device token"),
                ],
                max_length=40,
            ),
        ),
    ]
