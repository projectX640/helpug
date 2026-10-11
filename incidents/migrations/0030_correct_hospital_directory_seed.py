from django.contrib.auth.hashers import make_password
from django.db import migrations
from django.utils.text import slugify


SOURCE_URL = "https://nhfr.health.go.ug/"


def seed_missing_hospitals(apps, schema_editor):
    User = apps.get_model("auth", "User")
    LocationArea = apps.get_model("incidents", "LocationArea")
    HospitalFacility = apps.get_model("incidents", "HospitalFacility")
    InstitutionProfile = apps.get_model("incidents", "InstitutionProfile")
    password_hash = make_password("2564")

    HospitalFacility.objects.filter(name="Buhinga General Hospital").delete()

    for name, district_name, level in [
        ("Bukwo General Hospital", "Bukwo", "General Hospital"),
        ("Masafu General Hospital", "Busia", "General Hospital"),
    ]:
        district = LocationArea.objects.filter(name__iexact=district_name).first()
        if district is None:
            district = LocationArea.objects.create(name=district_name, district=district_name, active=True)
        facility, _ = HospitalFacility.objects.get_or_create(
            name=name,
            district=district,
            defaults={
                "ownership": "government",
                "level": level,
                "source_url": SOURCE_URL,
                "active": True,
            },
        )
        profile, _ = InstitutionProfile.objects.get_or_create(
            hospital_facility=facility,
            defaults={
                "username": slugify(f"{facility.name}-{district.name}")[:150],
                "institution_type": "hospital",
                "institution_name": facility.name,
                "area_id": district.pk,
                "active": True,
                "force_password_change": True,
            },
        )
        if profile.user_id is None:
            user, created = User.objects.get_or_create(
                username=profile.username,
                defaults={"password": password_hash, "is_active": True},
            )
            if created:
                user.password = password_hash
                user.save(update_fields=["password"])
            profile.user_id = user.pk
            profile.save(update_fields=["user"])


class Migration(migrations.Migration):
    dependencies = [("incidents", "0029_expand_uganda_hospital_directory")]

    operations = [migrations.RunPython(seed_missing_hospitals, migrations.RunPython.noop)]
