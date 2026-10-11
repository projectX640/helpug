from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("incidents", "0036_device_token_only_similarity"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="SecurityEvent",
            fields=[
                (
                    "id",
                    models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
                ),
                (
                    "event_type",
                    models.CharField(
                        choices=[
                            ("login_success", "Login succeeded"),
                            ("login_failure", "Login failed"),
                            ("login_throttled", "Login throttled"),
                            ("session_expired", "Session expired"),
                            ("access_denied", "Access denied"),
                        ],
                        max_length=32,
                    ),
                ),
                ("ip_address", models.GenericIPAddressField(blank=True, null=True)),
                ("path", models.CharField(blank=True, max_length=255)),
                ("method", models.CharField(blank=True, max_length=10)),
                ("details", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="security_events",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at", "-pk"],
                "indexes": [
                    models.Index(fields=["event_type", "created_at"], name="incidents_s_event_t_ccba25_idx"),
                    models.Index(fields=["user", "created_at"], name="incidents_s_user_id_3ea7c2_idx"),
                ],
            },
        ),
    ]
