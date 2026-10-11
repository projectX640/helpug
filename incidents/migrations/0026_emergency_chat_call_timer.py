from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("incidents", "0025_emergency_chat_call_controls"),
    ]

    operations = [
        migrations.AddField(
            model_name="emergencychatcall",
            name="started_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
