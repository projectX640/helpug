from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("incidents", "0020_seed_institution_accounts")]

    operations = [
        migrations.AddField(
            model_name="incident",
            name="opened_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
