from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("incidents", "0005_normalize_device_metadata")]
    operations = [
        migrations.AddField(
            model_name="locationarea",
            name="routing_code",
            field=models.CharField(blank=True, max_length=8, null=True, unique=True),
        ),
    ]
