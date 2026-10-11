from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("incidents", "0026_emergency_chat_call_timer"),
    ]

    operations = [
        migrations.AddField(
            model_name="emergencychatmessage",
            name="channel",
            field=models.CharField(choices=[("text", "Text message"), ("audio", "Audio note"), ("system", "System event")], default="text", max_length=20),
        ),
        migrations.AddField(
            model_name="emergencychatmessage",
            name="idempotency_key",
            field=models.CharField(blank=True, editable=False, max_length=64, null=True, unique=True),
        ),
    ]
