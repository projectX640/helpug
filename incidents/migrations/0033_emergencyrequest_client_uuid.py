from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("incidents", "0032_inhouse_admin_chat")]

    operations = [
        migrations.AddField(
            model_name="emergencyrequest",
            name="client_uuid",
            field=models.UUIDField(blank=True, db_index=True, null=True),
        ),
    ]
