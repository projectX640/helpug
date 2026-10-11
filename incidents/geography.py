import json
from functools import lru_cache
from pathlib import Path


BOUNDARY_FILE = Path(__file__).resolve().parent / "data" / "uganda_districts.geojson"
BOUNDARY_AREA_ALIASES = {
    "Luwero": "Luweero",
}


def _coordinates_bbox(coordinates):
    points = []
    stack = [coordinates]
    while stack:
        item = stack.pop()
        if item and isinstance(item[0], (int, float)):
            points.append(item)
        else:
            stack.extend(item)
    longitudes = [point[0] for point in points]
    latitudes = [point[1] for point in points]
    return min(longitudes), min(latitudes), max(longitudes), max(latitudes)


@lru_cache(maxsize=1)
def district_boundaries():
    data = json.loads(BOUNDARY_FILE.read_text(encoding="utf-8"))
    boundaries = []
    for feature in data.get("features", []):
        properties = feature.get("properties", {})
        geometry = feature.get("geometry") or {}
        coordinates = geometry.get("coordinates") or []
        if not coordinates:
            continue
        boundaries.append({
            "name": properties.get("name", "").strip(),
            "geometry": geometry,
            "bbox": _coordinates_bbox(coordinates),
        })
    return tuple(boundaries)


def _point_on_segment(point_x, point_y, start, end):
    start_x, start_y = start
    end_x, end_y = end
    cross_product = (point_y - start_y) * (end_x - start_x) - (point_x - start_x) * (end_y - start_y)
    if abs(cross_product) > 1e-10:
        return False
    return min(start_x, end_x) - 1e-10 <= point_x <= max(start_x, end_x) + 1e-10 and min(start_y, end_y) - 1e-10 <= point_y <= max(start_y, end_y) + 1e-10


def _point_in_ring(point_x, point_y, ring):
    inside = False
    for index, start in enumerate(ring):
        end = ring[(index + 1) % len(ring)]
        if _point_on_segment(point_x, point_y, start, end):
            return True
        start_x, start_y = start
        end_x, end_y = end
        crosses_latitude = (start_y > point_y) != (end_y > point_y)
        if crosses_latitude:
            intersection_x = (end_x - start_x) * (point_y - start_y) / (end_y - start_y) + start_x
            if point_x < intersection_x:
                inside = not inside
    return inside


def _point_in_polygon(point_x, point_y, polygon):
    if not polygon or not _point_in_ring(point_x, point_y, polygon[0]):
        return False
    return not any(_point_in_ring(point_x, point_y, hole) for hole in polygon[1:])


def _point_in_geometry(point_x, point_y, geometry):
    geometry_type = geometry.get("type")
    coordinates = geometry.get("coordinates") or []
    if geometry_type == "Polygon":
        return _point_in_polygon(point_x, point_y, coordinates)
    if geometry_type == "MultiPolygon":
        return any(_point_in_polygon(point_x, point_y, polygon) for polygon in coordinates)
    return False


def boundary_name_for_point(latitude, longitude):
    point_x = float(longitude)
    point_y = float(latitude)
    for boundary in district_boundaries():
        west, south, east, north = boundary["bbox"]
        if west <= point_x <= east and south <= point_y <= north and _point_in_geometry(point_x, point_y, boundary["geometry"]):
            return boundary["name"]
    return None


def boundary_features(area_names=None):
    allowed_names = set(area_names) if area_names is not None else None
    features = []
    for boundary in district_boundaries():
        if allowed_names is not None and boundary["name"] not in allowed_names:
            continue
        features.append({
            "type": "Feature",
            "properties": {"name": boundary["name"]},
            "geometry": boundary["geometry"],
        })
    return {"type": "FeatureCollection", "features": features}


def area_name_for_boundary(boundary_name, available_names):
    if not boundary_name:
        return None
    available = set(available_names)
    if boundary_name in available:
        return boundary_name
    alias = BOUNDARY_AREA_ALIASES.get(boundary_name)
    if alias in available:
        return alias
    city_name = f"{boundary_name} City"
    if city_name in available:
        return city_name
    return None
