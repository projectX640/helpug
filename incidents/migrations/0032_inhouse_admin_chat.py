from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("incidents", "0031_remove_orphaned_hospital_profile"),
    ]

    operations = [
        migrations.CreateModel(
            name="InHouseConversation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user_one", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="inhouse_conversations_as_one", to=settings.AUTH_USER_MODEL)),
                ("user_two", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="inhouse_conversations_as_two", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-updated_at", "-pk"]},
        ),
        migrations.CreateModel(
            name="InHouseMessage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("body", models.TextField(max_length=4000)),
                ("idempotency_key", models.CharField(blank=True, editable=False, max_length=64, null=True, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("read_at", models.DateTimeField(blank=True, null=True)),
                ("conversation", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="messages", to="incidents.inhouseconversation")),
                ("recipient", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="inhouse_messages_received", to=settings.AUTH_USER_MODEL)),
                ("sender", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="inhouse_messages_sent", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["created_at", "pk"]},
        ),
        migrations.AddConstraint(
            model_name="inhouseconversation",
            constraint=models.UniqueConstraint(fields=("user_one", "user_two"), name="unique_inhouse_user_pair"),
        ),
    ]
