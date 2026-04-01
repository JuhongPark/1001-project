"""LightMap Boston - FastAPI backend.

Serves shadow/brightness data and static frontend files.
"""

import csv
import json
import os
import time
from datetime import datetime
from zoneinfo import ZoneInfo

import httpx
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from shadow.compute import compute_all_shadows, get_sun_position

app = FastAPI(title="LightMap Boston")

DATA = os.path.join(os.path.dirname(__file__), "..", "data")
STATIC = os.path.join(os.path.dirname(__file__), "static")
BOSTON_TZ = ZoneInfo("US/Eastern")

WEATHER_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=42.36&longitude=-71.06"
    "&current=temperature_2m,relative_humidity_2m,"
    "precipitation,weather_code,wind_speed_10m,uv_index"
)
AQI_URL = (
    "https://air-quality-api.open-meteo.com/v1/air-quality"
    "?latitude=42.36&longitude=-71.06"
    "&current=us_aqi,pm2_5"
)

WMO_DESCRIPTIONS = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}

WEATHER_CACHE_TTL = 300
_weather_cache = None
_weather_cache_time = 0

_streetlight_cache = None
_business_cache = None
_building_geojson_cache = None
_flood_cache = None
_ice_cache = None
_crime_night_cache = None
_canopy_cache = None
_canopy_density_cache = None

SHADOW_CACHE_MAX = 48
_shadow_cache = {}


def _round_to_30min(dt: datetime) -> tuple:
    """Round datetime to nearest 30-min interval, return cache key."""
    minute = 0 if dt.minute < 15 else (30 if dt.minute < 45 else 0)
    hour = dt.hour if dt.minute < 45 else dt.hour + 1
    if hour >= 24:
        hour = 0
    return (dt.date().isoformat(), hour, minute)

DEFAULT_WEATHER = {
    "temperature_f": 0,
    "temperature_c": 0,
    "humidity": 0,
    "precipitation_mm": 0,
    "weather_code": 0,
    "weather_description": "Unavailable",
    "wind_speed_mph": 0,
    "uv_index": 0,
    "aqi": 0,
    "pm25": 0.0,
    "is_raining": False,
    "is_freezing": False,
}


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
    """Return shadow GeoJSON for a given time.

    Results are cached per 30-min interval (up to 48 entries).
    First request for a slot computes shadows; subsequent requests are instant.
    """
    global _shadow_cache
    dt = parse_time(time)
    cache_key = _round_to_30min(dt)

    if cache_key in _shadow_cache:
        return _shadow_cache[cache_key]

    buildings_path = os.path.join(DATA, "buildings", "all_buildings.geojson")
    shadows, altitude, azimuth = compute_all_shadows(buildings_path, dt)
    result = {
        "type": "FeatureCollection",
        "features": shadows,
        "metadata": {
            "time": dt.isoformat(),
            "sun_altitude": round(float(altitude), 2),
            "sun_azimuth": round(float(azimuth), 2),
            "building_count": len(shadows),
            "cached": False,
        },
    }

    if len(_shadow_cache) >= SHADOW_CACHE_MAX:
        oldest_key = next(iter(_shadow_cache))
        del _shadow_cache[oldest_key]
    _shadow_cache[cache_key] = result

    return result


@app.get("/api/streetlights")
def get_streetlights():
    """Return Boston + Cambridge streetlight locations as compact coordinate array."""
    global _streetlight_cache
    if _streetlight_cache is not None:
        return _streetlight_cache

    coords = []
    boston_path = os.path.join(DATA, "streetlights", "streetlights.csv")
    with open(boston_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                lat = float(row["Lat"])
                lon = float(row["Long"])
                if lat and lon:
                    coords.append([round(lon, 6), round(lat, 6)])
            except (ValueError, KeyError):
                continue

    cambridge_path = os.path.join(DATA, "cambridge", "streetlights", "streetlights.geojson")
    if os.path.exists(cambridge_path):
        with open(cambridge_path) as f:
            cdata = json.load(f)
        for feat in cdata.get("features", []):
            c = feat.get("geometry", {}).get("coordinates")
            if c and len(c) >= 2:
                coords.append([round(c[0], 6), round(c[1], 6)])

    _streetlight_cache = {"coords": coords}
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

    path = os.path.join(DATA, "buildings", "all_buildings.geojson")
    with open(path) as f:
        _building_geojson_cache = json.load(f)
    return _building_geojson_cache


@app.get("/api/canopy")
def get_canopy():
    """Return tree canopy polygons as GeoJSON (cached after first load)."""
    global _canopy_cache
    if _canopy_cache is not None:
        return _canopy_cache

    path = os.path.join(DATA, "trees", "all_canopy.geojson")
    with open(path) as f:
        _canopy_cache = json.load(f)
    return _canopy_cache


@app.get("/api/canopy/density")
def get_canopy_density():
    """Return tree canopy centroids as compact coordinate array for heatmap."""
    global _canopy_density_cache
    if _canopy_density_cache is not None:
        return _canopy_density_cache

    path = os.path.join(DATA, "trees", "canopy_centroids.json")
    with open(path) as f:
        _canopy_density_cache = json.load(f)
    return _canopy_density_cache


def _load_complaint_coords(filepaths, lat_col="latitude", lon_col="longitude"):
    """Load lat/lon from one or more CSV files, return compact coord array."""
    coords = []
    for path in filepaths:
        if not os.path.exists(path):
            continue
        with open(path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    lat = float(row[lat_col])
                    lon = float(row[lon_col])
                    if lat and lon:
                        coords.append([round(lon, 6), round(lat, 6)])
                except (ValueError, KeyError):
                    continue
    return coords


@app.get("/api/hazards/flood")
def get_flood_data():
    """Return flood complaint locations (Boston + Cambridge)."""
    global _flood_cache
    if _flood_cache is not None:
        return _flood_cache
    boston = os.path.join(DATA, "weather", "flood_complaints.csv")
    cambridge = os.path.join(DATA, "cambridge", "weather", "flood_complaints.csv")
    boston_coords = _load_complaint_coords([boston])
    cambridge_coords = _load_complaint_coords([cambridge], lat_col="lat", lon_col="lng")
    _flood_cache = {"coords": boston_coords + cambridge_coords}
    return _flood_cache


@app.get("/api/hazards/ice")
def get_ice_data():
    """Return ice/snow complaint locations (Boston + Cambridge)."""
    global _ice_cache
    if _ice_cache is not None:
        return _ice_cache
    boston = os.path.join(DATA, "weather", "ice_complaints.csv")
    cambridge = os.path.join(DATA, "cambridge", "weather", "ice_complaints.csv")
    boston_coords = _load_complaint_coords([boston])
    cambridge_coords = _load_complaint_coords([cambridge], lat_col="lat", lon_col="lng")
    _ice_cache = {"coords": boston_coords + cambridge_coords}
    return _ice_cache


@app.get("/api/safety/nighttime")
def get_nighttime_safety():
    """Return nighttime crime/crash density (Boston + Cambridge, hours 18-6)."""
    global _crime_night_cache
    if _crime_night_cache is not None:
        return _crime_night_cache

    coords = []
    boston_crime = os.path.join(DATA, "safety", "crime_incidents.csv")
    if os.path.exists(boston_crime):
        with open(boston_crime) as f:
            for row in csv.DictReader(f):
                try:
                    hour = int(row.get("HOUR", -1))
                    if hour >= 18 or hour <= 6:
                        lat = float(row["Lat"])
                        lon = float(row["Long"])
                        if lat and lon:
                            coords.append([round(lon, 6), round(lat, 6)])
                except (ValueError, KeyError):
                    continue

    cambridge_crime = os.path.join(DATA, "cambridge", "safety", "crime_incidents.csv")
    if os.path.exists(cambridge_crime):
        with open(cambridge_crime) as f:
            for row in csv.DictReader(f):
                try:
                    ts = row.get("crime_date_time", "")
                    if "T" in ts:
                        hour = int(ts.split("T")[1].split(":")[0])
                    else:
                        continue
                    if hour >= 18 or hour <= 6:
                        lat = float(row.get("reporting_area_lat", 0))
                        lon = float(row.get("reporting_area_lon", 0))
                        if lat and lon:
                            coords.append([round(lon, 6), round(lat, 6)])
                except (ValueError, KeyError):
                    continue

    _crime_night_cache = {"coords": coords}
    return _crime_night_cache


def _fetch_weather():
    """Fetch weather and AQI data from Open-Meteo APIs."""
    global _weather_cache, _weather_cache_time
    now = time.time()
    if _weather_cache is not None and (now - _weather_cache_time) < WEATHER_CACHE_TTL:
        return _weather_cache

    try:
        with httpx.Client(timeout=5.0) as client:
            weather_req = client.build_request("GET", WEATHER_URL)
            aqi_req = client.build_request("GET", AQI_URL)
            weather_resp = client.send(weather_req)
            aqi_resp = client.send(aqi_req)

        weather_resp.raise_for_status()
        aqi_resp.raise_for_status()
        w = weather_resp.json()["current"]
        a = aqi_resp.json()["current"]

        temp_c = w.get("temperature_2m", 0)
        temp_f = round(temp_c * 9 / 5 + 32)
        weather_code = w.get("weather_code", 0)
        precip = w.get("precipitation", 0)
        wind_kmh = w.get("wind_speed_10m", 0)

        rain_codes = {51, 53, 55, 61, 63, 65, 80, 81, 82, 95, 96, 99}

        result = {
            "temperature_f": temp_f,
            "temperature_c": round(temp_c, 1),
            "humidity": w.get("relative_humidity_2m", 0),
            "precipitation_mm": round(precip, 1),
            "weather_code": weather_code,
            "weather_description": WMO_DESCRIPTIONS.get(weather_code, "Unknown"),
            "wind_speed_mph": round(wind_kmh * 0.621371),
            "uv_index": w.get("uv_index", 0),
            "aqi": a.get("us_aqi", 0),
            "pm25": round(a.get("pm2_5", 0), 1),
            "is_raining": weather_code in rain_codes or precip > 0,
            "is_freezing": temp_c <= 0,
        }

        _weather_cache = result
        _weather_cache_time = now
        return result
    except Exception:
        if _weather_cache is not None:
            return _weather_cache
        return dict(DEFAULT_WEATHER)


@app.get("/api/weather")
def get_weather():
    """Return current weather and air quality for Boston."""
    return _fetch_weather()


@app.get("/api/debug")
def debug_log(msg: str = Query("")):
    """Receive debug messages from frontend."""
    print(f"[FRONTEND] {msg}")
    return {"ok": True}


@app.get("/")
def index():
    return FileResponse(os.path.join(STATIC, "index.html"))


app.mount("/static", StaticFiles(directory=STATIC), name="static")
