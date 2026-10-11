from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("incidents", "0010_responseprofile_favorites_passcode_hash"),
    ]

    operations = [
        migrations.CreateModel(
            name="ReferralDestination",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=180)),
                ("destination_type", models.CharField(choices=[("police_station", "Police station"), ("hospital", "Hospital"), ("government", "Government institution"), ("company", "Company / organisation")], max_length=30)),
                ("contact", models.CharField(blank=True, max_length=160)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("active", models.BooleanField(default=True)),
                ("area", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="referral_destinations", to="incidents.locationarea")),
                ("assigned_admin", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="referral_destinations", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["destination_type", "name"]},
        ),
        migrations.AddField(
            model_name="referral",
            name="destination",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="referrals", to="incidents.referraldestination"),
        ),
        migrations.AddField(
            model_name="referral",
            name="recipient_admin",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="received_referrals", to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name="referral",
            name="read_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
