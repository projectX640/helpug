from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("incidents", "0021_incident_opened_at")]

    operations = [
        migrations.AddField(
            model_name="referral",
            name="referral_token_hash",
            field=models.CharField(blank=True, editable=False, max_length=64),
        ),
    ]
