from django.db import migrations


ADDITIONAL_LOCATIONS = [
    "Hoima City", "Jinja City", "Lira City", "Masaka City", "Mbale City",
    "Mbarara City", "Soroti City", "Arua City", "Fort Portal City", "Gulu City",
    "Kagadi", "Kakumiro", "Kapelebyong", "Karenga", "Kasese", "Kiryandongo", "Yumbe",
]


def seed_missing_locations(apps, schema_editor):
    location_area = apps.get_model("incidents", "LocationArea")
    for location in ADDITIONAL_LOCATIONS:
        location_area.objects.get_or_create(
            name=location,
            defaults={"district": location, "active": True},
        )


class Migration(migrations.Migration):
    dependencies = [("incidents", "0003_seed_uganda_districts")]
    operations = [migrations.RunPython(seed_missing_locations, migrations.RunPython.noop)]
