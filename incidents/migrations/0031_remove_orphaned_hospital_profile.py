from django.db import migrations


def remove_orphaned_profile(apps, schema_editor):
    InstitutionProfile = apps.get_model("incidents", "InstitutionProfile")
    InstitutionProfile.objects.filter(
        institution_type="hospital",
        hospital_facility__isnull=True,
        institution_name="Buhinga General Hospital",
    ).delete()


class Migration(migrations.Migration):
    dependencies = [("incidents", "0030_correct_hospital_directory_seed")]

    operations = [migrations.RunPython(remove_orphaned_profile, migrations.RunPython.noop)]
