import re

from .models import LocationArea


def matching_area_names(area):
    name = area.name.strip()
    base_name = re.sub(r"\s+City$", "", name, flags=re.IGNORECASE)
    names = {name, base_name}
    if base_name == name:
        names.add(f"{name} City")
    return names


def matching_area_ids(area_id):
    try:
        area = LocationArea.objects.filter(pk=area_id, active=True).first()
    except (TypeError, ValueError):
        return []
    if area is None:
        return []
    return LocationArea.objects.filter(
        active=True,
        name__in=matching_area_names(area),
    ).values_list("pk", flat=True)
