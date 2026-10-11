from django.contrib.auth.hashers import make_password
from django.db import migrations
from django.utils.text import slugify


SOURCE_URL = "https://nhfr.health.go.ug/"

GOVERNMENT_HOSPITALS = [
    ("Abim General Hospital", "Abim", "General Hospital"),
    ("Adjumani General Hospital", "Adjumani", "General Hospital"),
    ("Amuria General Hospital", "Amuria", "General Hospital"),
    ("Anaka General Hospital", "Amuru", "General Hospital"),
    ("Apac General Hospital", "Apac", "General Hospital"),
    ("Atutur General Hospital", "Kumi", "General Hospital"),
    ("Bombo General Military Hospital", "Luweero", "General Hospital"),
    ("Bududa General Hospital", "Bududa", "General Hospital"),
    ("Bugiri General Hospital", "Bugiri", "General Hospital"),
    ("Bukwo General Hospital", "Bukwo", "General Hospital"),
    ("Buliisa General Hospital", "Buliisa", "General Hospital"),
    ("Bundibugyo General Hospital", "Bundibugyo", "General Hospital"),
    ("Buwenge General Hospital", "Jinja", "General Hospital"),
    ("Bwera General Hospital", "Kasese", "General Hospital"),
    ("Busolwe General Hospital", "Butaleja", "General Hospital"),
    ("Gombe General Hospital", "Butambala", "General Hospital"),
    ("Gulu Military General Hospital", "Gulu", "General Hospital"),
    ("Entebbe General Hospital", "Wakiso", "General Hospital"),
    ("Itojo General Hospital", "Ntungamo", "General Hospital"),
    ("Kaabong General Hospital", "Kaabong", "General Hospital"),
    ("Kaberamaido General Hospital", "Kaberamaido", "General Hospital"),
    ("Kagadi General Hospital", "Kagadi", "General Hospital"),
    ("Kalisizo General Hospital", "Kyotera", "General Hospital"),
    ("Kambuga General Hospital", "Kanungu", "General Hospital"),
    ("Kamuli General Hospital", "Kamuli", "General Hospital"),
    ("Kapchorwa General Hospital", "Kapchorwa", "General Hospital"),
    ("Katakwi General Hospital", "Katakwi", "General Hospital"),
    ("Kawolo General Hospital", "Buikwe", "General Hospital"),
    ("Kiboga General Hospital", "Kiboga", "General Hospital"),
    ("Kiryandongo General Hospital", "Kiryandongo", "General Hospital"),
    ("Kisoro General Hospital", "Kisoro", "General Hospital"),
    ("Kitagata General Hospital", "Sheema", "General Hospital"),
    ("Kitgum General Hospital", "Kitgum", "General Hospital"),
    ("Koboko General Hospital", "Koboko", "General Hospital"),
    ("Kotido General Hospital", "Kotido", "General Hospital"),
    ("Kyegegwa General Hospital", "Kyegegwa", "General Hospital"),
    ("Kyenjojo General Hospital", "Kyenjojo", "General Hospital"),
    ("Luwero General Hospital", "Luweero", "General Hospital"),
    ("Lyantonde General Hospital", "Lyantonde", "General Hospital"),
    ("Moyo General Hospital", "Moyo", "General Hospital"),
    ("Mpigi Hospital", "Mpigi", "General Hospital"),
    ("Mukono General Hospital", "Mukono", "General Hospital"),
    ("Nakaseke General Hospital", "Nakaseke", "General Hospital"),
    ("Nakasongola Military General Hospital", "Nakasongola", "General Hospital"),
    ("Murchison Bay Prison General Hospital", "Kampala", "General Hospital"),
    ("Masafu General Hospital", "Busia", "General Hospital"),
    ("Pallisa General Hospital", "Pallisa", "General Hospital"),
    ("Rakai General Hospital", "Rakai", "General Hospital"),
    ("Rukunyu General Hospital", "Kamwenge", "General Hospital"),
    ("Yumbe General Hospital", "Yumbe", "General Hospital"),
    ("Butabika National Referral Hospital", "Kampala", "National Referral Hospital"),
    ("China-Uganda Friendship Hospital Naguru", "Kampala", "National Referral Hospital"),
    ("Mulago Specialized Women and Neonatal Hospital", "Kampala", "National Referral Hospital"),
    ("Uganda Cancer Institute", "Kampala", "National Referral Hospital"),
    ("Uganda Heart Institute", "Kampala", "National Referral Hospital"),
    ("Entebbe Regional Referral Hospital", "Wakiso", "Regional Referral Hospital"),
    ("Kayunga Regional Referral Hospital", "Kayunga", "Regional Referral Hospital"),
    ("Yumbe Regional Referral Hospital", "Yumbe", "Regional Referral Hospital"),
]


def seed_hospitals_and_accounts(apps, schema_editor):
    User = apps.get_model("auth", "User")
    LocationArea = apps.get_model("incidents", "LocationArea")
    HospitalFacility = apps.get_model("incidents", "HospitalFacility")
    InstitutionProfile = apps.get_model("incidents", "InstitutionProfile")
    password_hash = make_password("2564")

    for name, district_name, level in GOVERNMENT_HOSPITALS:
        district = LocationArea.objects.filter(name__iexact=district_name).first()
        if district is None:
            district = LocationArea.objects.create(
                name=district_name,
                district=district_name,
                active=True,
            )
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
        InstitutionProfile.objects.get_or_create(
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
        profile = InstitutionProfile.objects.filter(hospital_facility=facility).select_related("user").first()
        if profile and profile.user_id is None:
            username = profile.username
            user, created = User.objects.get_or_create(
                username=username,
                defaults={"password": password_hash, "is_active": True},
            )
            if created:
                user.password = password_hash
                user.save(update_fields=["password"])
            profile.user_id = user.pk
            profile.save(update_fields=["user"])


class Migration(migrations.Migration):
    dependencies = [("incidents", "0028_write_idempotency_and_locks")]

    operations = [migrations.RunPython(seed_hospitals_and_accounts, migrations.RunPython.noop)]
