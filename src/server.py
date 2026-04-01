"""LightMap Boston - FastAPI backend.

Serves shadow/brightness data and static frontend files.
"""

import csv
import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from shadow.compute import compute_all_shadows, get_sun_position

app = FastAPI(title="LightMap Boston")

DATA = os.path.join(os.path.dirname(__file__), "..", "data")
STATIC = os.path.join(os.path.dirname(__file__), "static")
BOSTON_TZ = ZoneInfo("US/Eastern")

# Cache static data that doesn't change between requests
_streetlight_cache = None
_business_cache = None
_building_geojson_cache = None


def parse_time(time_str: str | None) -> datetime:
    """Parse ISO time string or return current Boston time."""
    if time_str:
        dt = datetime.fromisoformat(time_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=BOSTON_TZ)
        return dt
    return datetime.now(BOSTON_TZ)


@app.get("/api/info")
def get_info(time: str | None = Query(None)):
    """Return sun position and mode for a given time."""
    dt = parse_time(time)
    altitude, azimuth = get_sun_position(dt)
    is_day = bool(altitude > 0)
    return {
        "time": dt.isoformat(),
        "sun_altitude": round(float(altitude), 2),
        "sun_azimuth": round(float(azimuth), 2),
        "is_day": is_day,
        "mode": "day" if is_day else "night",
    }


@app.get("/api/shadows")
def get_shadows(time: str | None = Query(None)):
    """Return shadow GeoJSON for a given time."""
    dt = parse_time(time)
    buildings_path = os.path.join(DATA, "buildings", "buildings_sample.geojson")
    shadows, altitude, azimuth = compute_all_shadows(buildings_path, dt)
    return {
        "type": "FeatureCollection",
        "features": shadows,
        "metadata": {
            "time": dt.isoformat(),
            "sun_altitude": round(float(altitude), 2),
            "sun_azimuth": round(float(azimuth), 2),
            "building_count": len(shadows),
        },
    }


@app.get("/api/streetlights")
def get_streetlights():
    """Return streetlight locations as GeoJSON (cached after first load)."""
    global _streetlight_cache
    if _streetlight_cache is not None:
        return _streetlight_cache

    path = os.path.join(DATA, "streetlights", "streetlights.csv")
    features = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                lat = float(row["Lat"])
                lon = float(row["Long"])
                if lat and lon:
                    features.append({
                        "type": "Feature",
                        "geometry": {"type": "Point", "coordinates": [lon, lat]},
                        "properties": {},
                    })
            except (ValueError, KeyError):
                continue
    _streetlight_cache = {"type": "FeatureCollection", "features": features}
    return _streetlight_cache


@app.get("/api/businesses")
def get_businesses():
    """Return food establishment locations as GeoJSON (cached after first load)."""
    global _business_cache
    if _business_cache is not None:
        return _business_cache

    path = os.path.join(DATA, "safety", "food_establishments.csv")
    features = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                lat = float(row["latitude"])
                lon = float(row["longitude"])
                name = row.get("businessname", "")
                if lat and lon:
                    features.append({
                        "type": "Feature",
                        "geometry": {"type": "Point", "coordinates": [lon, lat]},
                        "properties": {"name": name},
                    })
            except (ValueError, KeyError):
                continue
    _business_cache = {"type": "FeatureCollection", "features": features}
    return _business_cache


@app.get("/api/buildings")
def get_buildings():
    """Return building footprints as GeoJSON (cached after first load)."""
    global _building_geojson_cache
    if _building_geojson_cache is not None:
        return _building_geojson_cache

    path = os.path.join(DATA, "buildings", "buildings_sample.geojson")
    with open(path) as f:
        _building_geojson_cache = json.load(f)
    return _building_geojson_cache


@app.get("/api/debug")
def debug_log(msg: str = Query("")):
    """Receive debug messages from frontend."""
    print(f"[FRONTEND] {msg}")
    return {"ok": True}


@app.get("/")
def index():
    return FileResponse(os.path.join(STATIC, "index.html"))


app.mount("/static", StaticFiles(directory=STATIC), name="static")
