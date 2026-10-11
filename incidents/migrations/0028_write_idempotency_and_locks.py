from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("incidents", "0027_emergency_chat_message_channels"),
    ]

    operations = [
        migrations.AddField(
            model_name="referral",
            name="idempotency_key",
            field=models.CharField(blank=True, editable=False, max_length=64, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="incidentnote",
            name="idempotency_key",
            field=models.CharField(blank=True, editable=False, max_length=64, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="casemessage",
            name="idempotency_key",
            field=models.CharField(blank=True, editable=False, max_length=64, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="callrequest",
            name="idempotency_key",
            field=models.CharField(blank=True, editable=False, max_length=64, null=True, unique=True),
        ),
        migrations.AddConstraint(
            model_name="emergencychatcall",
            constraint=models.UniqueConstraint(
                condition=models.Q(status="requested"),
                fields=("room",),
                name="unique_requested_emergency_call",
            ),
        ),
        migrations.AddConstraint(
            model_name="callrequest",
            constraint=models.UniqueConstraint(
                condition=models.Q(status="requested"),
                fields=("referral",),
                name="unique_requested_referral_call",
            ),
        ),
    ]
