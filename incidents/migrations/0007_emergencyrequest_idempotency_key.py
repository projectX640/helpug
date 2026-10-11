from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("incidents", "0006_locationarea_routing_code")]

    operations = [
        migrations.AddField(
            model_name="emergencyrequest",
            name="idempotency_key",
            field=models.CharField(blank=True, editable=False, max_length=64, null=True, unique=True),
        ),
    ]
