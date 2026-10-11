from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("incidents", "0022_referral_referral_token_hash")]

    operations = [
        migrations.CreateModel(
            name="EmergencyChatRoom",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("accepted_at", models.DateTimeField(blank=True, null=True)),
                ("expires_at", models.DateTimeField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("incident", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="emergency_chat_room", to="incidents.incident")),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="EmergencyChatMessage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("sender_type", models.CharField(choices=[("public", "Request sender"), ("admin", "Responder admin"), ("system", "System")], max_length=20)),
                ("body", models.TextField(blank=True, max_length=4000)),
                ("audio", models.FileField(blank=True, upload_to="emergency_chat_audio/")),
                ("audio_duration_seconds", models.PositiveIntegerField(blank=True, null=True)),
                ("read_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("room", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="messages", to="incidents.emergencychatroom")),
                ("sender", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="emergency_chat_messages", to="auth.user")),
            ],
            options={"ordering": ["created_at"]},
        ),
        migrations.CreateModel(
            name="EmergencyChatCall",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("requester_type", models.CharField(choices=[("public", "Request sender"), ("admin", "Responder admin")], max_length=20)),
                ("status", models.CharField(choices=[("requested", "Requested"), ("accepted", "Accepted"), ("declined", "Declined"), ("ended", "Ended")], default="requested", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("responded_at", models.DateTimeField(blank=True, null=True)),
                ("requested_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="emergency_chat_calls", to="auth.user")),
                ("room", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="calls", to="incidents.emergencychatroom")),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
