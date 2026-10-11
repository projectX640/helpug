from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("incidents", "0012_alter_referral_channel_alter_referral_target_type")]

    operations = [
        migrations.AddField(
            model_name="referral",
            name="destination_area",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="direct_referrals", to="incidents.locationarea"),
        ),
    ]
