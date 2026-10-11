from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("incidents", "0033_emergencyrequest_client_uuid")]

    operations = [
        migrations.AddField(
            model_name="emergencyrequest",
            name="last_location_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="emergencyrequest",
            name="tracking_active",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="emergencyrequest",
            name="tracking_enabled",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="emergencyrequest",
            name="tracking_started_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="emergencyrequest",
            name="tracking_stopped_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name="LocationPing",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("latitude", models.DecimalField(decimal_places=6, max_digits=9)),
                ("longitude", models.DecimalField(decimal_places=6, max_digits=9)),
                ("location_accuracy", models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ("idempotency_key", models.CharField(editable=False, max_length=64, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("request", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="location_pings", to="incidents.emergencyrequest")),
            ],
            options={"ordering": ["-created_at", "-pk"]},
        ),
    ]
