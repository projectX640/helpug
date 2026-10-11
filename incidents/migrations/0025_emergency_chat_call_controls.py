from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("incidents", "0024_emergency_chat_call_recipient"),
    ]

    operations = [
        migrations.AddField(
            model_name="emergencychatcall",
            name="on_hold",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="emergencychatcall",
            name="caller_muted",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="emergencychatcall",
            name="recipient_muted",
            field=models.BooleanField(default=False),
        ),
    ]
