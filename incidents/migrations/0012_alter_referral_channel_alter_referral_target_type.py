from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("incidents", "0011_referral_destinations_and_routing")]

    operations = [
        migrations.AlterField(
            model_name="referral",
            name="channel",
            field=models.CharField(
                choices=[
                    ("in_app", "In-app transfer"),
                    ("whatsapp", "WhatsApp"),
                    ("email", "Email / Gmail"),
                    ("sms", "SMS / Messages"),
                ],
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="referral",
            name="target_type",
            field=models.CharField(
                choices=[
                    ("admin", "Another responder admin"),
                    ("person", "Person"),
                    ("police_station", "Police station"),
                    ("hospital", "Hospital"),
                    ("company", "Company / organisation"),
                    ("government", "Government institution"),
                    ("organization", "Organisation / office"),
                ],
                max_length=20,
            ),
        ),
    ]
