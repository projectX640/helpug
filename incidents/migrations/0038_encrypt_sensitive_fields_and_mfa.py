from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

import incidents.fields


ENCRYPTED_FIELDS = {
    "casemessage": ("body",),
    "emergencychatmessage": ("body",),
    "emergencyrequest": (
        "ip_address",
        "latitude",
        "location_accuracy",
        "location_description",
        "longitude",
        "message",
        "phone_number",
    ),
    "incidentnote": ("note",),
    "inhousemessage": ("body",),
    "institutionprofile": ("phone_number",),
    "locationping": ("latitude", "location_accuracy", "longitude"),
    "referral": ("message", "target_contact"),
    "referraldestination": ("contact", "email"),
    "responseprofile": ("phone_number", "whatsapp_number"),
}


def encrypt_existing_values(apps, schema_editor):
    for model_name, field_names in ENCRYPTED_FIELDS.items():
        model = apps.get_model("incidents", model_name)
        for instance in model.objects.all().iterator():
            update_fields = []
            for field_name in field_names:
                value = getattr(instance, field_name)
                if value not in (None, ""):
                    setattr(instance, field_name, value)
                    update_fields.append(field_name)
            if update_fields:
                instance.save(update_fields=update_fields)


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("incidents", "0037_securityevent"),
    ]

    operations = [
        migrations.AlterField(
            model_name="casemessage",
            name="body",
            field=incidents.fields.EncryptedTextField(max_length=4000),
        ),
        migrations.AlterField(
            model_name="emergencychatmessage",
            name="body",
            field=incidents.fields.EncryptedTextField(blank=True, max_length=4000),
        ),
        migrations.AlterField(
            model_name="emergencyrequest",
            name="ip_address",
            field=incidents.fields.EncryptedTextField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name="emergencyrequest",
            name="latitude",
            field=incidents.fields.EncryptedDecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name="emergencyrequest",
            name="location_accuracy",
            field=incidents.fields.EncryptedDecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name="emergencyrequest",
            name="location_description",
            field=incidents.fields.EncryptedTextField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name="emergencyrequest",
            name="longitude",
            field=incidents.fields.EncryptedDecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name="emergencyrequest",
            name="message",
            field=incidents.fields.EncryptedTextField(blank=True),
        ),
        migrations.AlterField(
            model_name="emergencyrequest",
            name="phone_number",
            field=incidents.fields.EncryptedTextField(max_length=32),
        ),
        migrations.AlterField(
            model_name="incidentnote",
            name="note",
            field=incidents.fields.EncryptedTextField(max_length=2000),
        ),
        migrations.AlterField(
            model_name="inhousemessage",
            name="body",
            field=incidents.fields.EncryptedTextField(max_length=4000),
        ),
        migrations.AlterField(
            model_name="institutionprofile",
            name="phone_number",
            field=incidents.fields.EncryptedTextField(blank=True, max_length=32),
        ),
        migrations.AlterField(
            model_name="locationping",
            name="latitude",
            field=incidents.fields.EncryptedDecimalField(decimal_places=6, max_digits=9),
        ),
        migrations.AlterField(
            model_name="locationping",
            name="location_accuracy",
            field=incidents.fields.EncryptedDecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name="locationping",
            name="longitude",
            field=incidents.fields.EncryptedDecimalField(decimal_places=6, max_digits=9),
        ),
        migrations.AlterField(
            model_name="referral",
            name="message",
            field=incidents.fields.EncryptedTextField(),
        ),
        migrations.AlterField(
            model_name="referral",
            name="target_contact",
            field=incidents.fields.EncryptedTextField(max_length=160),
        ),
        migrations.AlterField(
            model_name="referraldestination",
            name="contact",
            field=incidents.fields.EncryptedTextField(blank=True, max_length=160),
        ),
        migrations.AlterField(
            model_name="referraldestination",
            name="email",
            field=incidents.fields.EncryptedTextField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name="responseprofile",
            name="phone_number",
            field=incidents.fields.EncryptedTextField(blank=True, max_length=32),
        ),
        migrations.AlterField(
            model_name="responseprofile",
            name="whatsapp_number",
            field=incidents.fields.EncryptedTextField(blank=True, max_length=32),
        ),
        migrations.AlterField(
            model_name="securityevent",
            name="event_type",
            field=models.CharField(
                choices=[
                    ("login_success", "Login succeeded"),
                    ("login_failure", "Login failed"),
                    ("login_throttled", "Login throttled"),
                    ("session_expired", "Session expired"),
                    ("access_denied", "Access denied"),
                    ("mfa_enabled", "MFA enabled"),
                    ("mfa_failure", "MFA failed"),
                ],
                max_length=32,
            ),
        ),
        migrations.CreateModel(
            name="MFAProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("secret", incidents.fields.EncryptedTextField(blank=True, editable=False)),
                ("enabled", models.BooleanField(default=False)),
                ("last_used_counter", models.BigIntegerField(blank=True, editable=False, null=True)),
                ("confirmed_at", models.DateTimeField(blank=True, editable=False, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="mfa_profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.RunPython(encrypt_existing_values, migrations.RunPython.noop),
    ]
