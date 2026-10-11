from django.db import migrations


def normalize_device_metadata(apps, schema_editor):
    from incidents.device_detection import detect_device

    emergency_request = apps.get_model("incidents", "EmergencyRequest")
    for request in emergency_request.objects.exclude(browser="").iterator():
        device = detect_device(request.browser)
        request.device_type = device["device_type"]
        request.operating_system = device["operating_system"]
        request.browser = device["browser"]
        request.save(update_fields=["device_type", "operating_system", "browser"])


class Migration(migrations.Migration):
    dependencies = [("incidents", "0004_seed_missing_uganda_locations")]
    operations = [migrations.RunPython(normalize_device_metadata, migrations.RunPython.noop)]
