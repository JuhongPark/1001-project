"""Shadow computation module for LightMap Boston."""

import math
import json
from datetime import datetime
from shapely.geometry import Polygon, MultiPolygon, mapping
from shapely.ops import unary_union
from pvlib.solarposition import get_solarposition
import pandas as pd


def get_sun_position(dt: datetime, lat: float = 42.36, lon: float = -71.06):
    """Get sun altitude and azimuth for Boston at a given datetime."""
    times = pd.DatetimeIndex([dt])
    pos = get_solarposition(times, lat, lon)
    altitude = pos.apparent_elevation.iloc[0]
    azimuth = pos.azimuth.iloc[0]
    return altitude, azimuth


def compute_shadow(building_polygon: Polygon, height_ft: float,
                   sun_altitude: float, sun_azimuth: float) -> Polygon:
    """Compute shadow polygon for a single building.

    Args:
        building_polygon: Building footprint in lon/lat (WGS84)
        height_ft: Building height in feet
        sun_altitude: Sun elevation angle in degrees
        sun_azimuth: Sun azimuth in degrees from north

    Returns:
        Shadow polygon in lon/lat, or None if sun is below horizon
    """
    if sun_altitude <= 0:
        return None

    height_m = height_ft * 0.3048
    shadow_length_m = height_m / math.tan(math.radians(sun_altitude))
    # Cap shadow length to 500m to avoid unrealistic polygons at very low sun angles
    shadow_length_m = min(shadow_length_m, 500)

    shadow_direction = math.radians(sun_azimuth + 180)

    dx_m = shadow_length_m * math.sin(shadow_direction)
    dy_m = shadow_length_m * math.cos(shadow_direction)

    lat_center = 42.36
    m_per_deg_lat = 111320
    m_per_deg_lon = 111320 * math.cos(math.radians(lat_center))

    dx_deg = dx_m / m_per_deg_lon
    dy_deg = dy_m / m_per_deg_lat

    shadow_coords = []
    for x, y in building_polygon.exterior.coords:
        shadow_coords.append((x + dx_deg, y + dy_deg))

    shadow_footprint = Polygon(shadow_coords)
    result = unary_union([building_polygon, shadow_footprint])

    if not result.is_valid:
        result = result.buffer(0)

    return result


_building_cache = {}


def compute_all_shadows(geojson_path: str, dt: datetime):
    """Compute shadows for all buildings in a GeoJSON file.

    Returns:
        List of shadow polygons as GeoJSON features
    """
    altitude, azimuth = get_sun_position(dt)

    if altitude <= 0:
        return [], altitude, azimuth

    if geojson_path not in _building_cache:
        with open(geojson_path) as f:
            _building_cache[geojson_path] = json.load(f)
    data = _building_cache[geojson_path]

    shadows = []
    for feature in data["features"]:
        height = feature["properties"].get("BLDG_HGT_2010", 0)
        if not height or height <= 0:
            continue

        geom = feature["geometry"]
        if geom["type"] == "Polygon":
            poly = Polygon(geom["coordinates"][0])
        elif geom["type"] == "MultiPolygon":
            polys = [Polygon(ring[0]) for ring in geom["coordinates"]]
            poly = unary_union(polys)
        else:
            continue

        if not poly.is_valid:
            poly = poly.buffer(0)

        shadow = compute_shadow(poly, height, altitude, azimuth)
        if shadow and shadow.is_valid:
            height_m = height * 0.3048
            shadow_len = min(height_m / math.tan(math.radians(altitude)), 500)
            shadows.append({
                "type": "Feature",
                "properties": {
                    "height_ft": round(height, 1),
                    "shadow_len_m": round(shadow_len, 1),
                    "type": "shadow"
                },
                "geometry": mapping(shadow)
            })

    return shadows, altitude, azimuth
