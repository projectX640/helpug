from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("incidents", "0023_emergency_chat"),
    ]

    operations = [
        migrations.AddField(
            model_name="emergencychatcall",
            name="recipient",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="emergency_chat_call_requests",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
