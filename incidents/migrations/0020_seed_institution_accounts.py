from django.contrib.auth.hashers import make_password
from django.db import migrations
from django.utils.text import slugify


def seed_institution_accounts(apps, schema_editor):
    User = apps.get_model("auth", "User")
    LocationArea = apps.get_model("incidents", "LocationArea")
    HospitalFacility = apps.get_model("incidents", "HospitalFacility")
    InstitutionProfile = apps.get_model("incidents", "InstitutionProfile")
    password_hash = make_password("2564")

    for area in LocationArea.objects.filter(active=True).order_by("pk"):
        username = area.name
        user, created = User.objects.get_or_create(
            username=username,
            defaults={"password": password_hash, "is_active": True},
        )
        if created:
            user.password = password_hash
            user.save(update_fields=["password"])
        InstitutionProfile.objects.get_or_create(
            username=username,
            defaults={
                "user_id": user.pk,
                "institution_type": "police",
                "institution_name": f"{area.name} Police Station",
                "area_id": area.pk,
                "active": True,
                "force_password_change": True,
            },
        )

    for facility in HospitalFacility.objects.filter(active=True).select_related("district"):
        username = slugify(f"{facility.name}-{facility.district.name}")[:150]
        user, created = User.objects.get_or_create(
            username=username,
            defaults={"password": password_hash, "is_active": True},
        )
        if created:
            user.password = password_hash
            user.save(update_fields=["password"])
        InstitutionProfile.objects.get_or_create(
            username=username,
            defaults={
                "user_id": user.pk,
                "institution_type": "hospital",
                "institution_name": facility.name,
                "area_id": facility.district_id,
                "hospital_facility_id": facility.pk,
                "active": True,
                "force_password_change": True,
            },
        )


class Migration(migrations.Migration):
    dependencies = [("incidents", "0019_hospitalfacility_and_more")]

    operations = [migrations.RunPython(seed_institution_accounts, migrations.RunPython.noop)]
