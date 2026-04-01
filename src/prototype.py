"""LightMap Boston - Prototype Map Generator.

Generates an interactive HTML map showing:
- Daytime: building shadows based on sun position
- Nighttime: streetlight locations as brightness indicators
"""

import csv
import json
import sys
import os
from datetime import datetime

import folium
from folium.plugins import HeatMap

sys.path.insert(0, os.path.dirname(__file__))
from shadow.compute import compute_all_shadows, get_sun_position

DATA = os.path.join(os.path.dirname(__file__), "..", "data")
OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "prototype.html")

BOSTON_CENTER = [42.355, -71.065]


def load_streetlights(max_count=None):
    """Load streetlight locations."""
    lights = []
    path = os.path.join(DATA, "streetlights", "streetlights.csv")
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                lat = float(row["Lat"])
                lon = float(row["Long"])
                if lat and lon:
                    lights.append([lat, lon])
            except (ValueError, KeyError):
                continue
            if max_count and len(lights) >= max_count:
                break
    return lights


def load_food_establishments():
    """Load food establishment locations."""
    places = []
    path = os.path.join(DATA, "safety", "food_establishments.csv")
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                lat = float(row["latitude"])
                lon = float(row["longitude"])
                name = row.get("businessname", "")
                if lat and lon:
                    places.append({"lat": lat, "lon": lon, "name": name})
            except (ValueError, KeyError):
                continue
    return places


def build_map(target_time: datetime = None):
    """Build the LightMap prototype."""
    if target_time is None:
        target_time = datetime.now().astimezone()

    altitude, azimuth = get_sun_position(target_time)
    is_day = altitude > 0

    print(f"Time: {target_time.strftime('%Y-%m-%d %H:%M %Z')}")
    print(f"Sun altitude: {altitude:.1f} deg, azimuth: {azimuth:.1f} deg")
    print(f"Mode: {'DAY (shadow map)' if is_day else 'NIGHT (brightness map)'}")

    if is_day:
        tiles = "CartoDB positron"
    else:
        tiles = "CartoDB dark_matter"

    m = folium.Map(
        location=BOSTON_CENTER,
        zoom_start=15,
        tiles=tiles,
    )

    info_text = f"""
    <div style="position:fixed; top:10px; left:60px; z-index:9999;
         background:{'#1e293b' if not is_day else 'white'};
         color:{'#e2e8f0' if not is_day else '#1e293b'};
         padding:12px 18px; border-radius:8px;
         font-family:system-ui; font-size:13px;
         box-shadow:0 2px 8px rgba(0,0,0,0.3);">
        <b>LightMap Boston</b> {'☀️' if is_day else '🌙'}<br>
        {target_time.strftime('%b %d, %Y %I:%M %p')}<br>
        Sun: {altitude:.1f}° alt, {azimuth:.1f}° az<br>
        Mode: <b>{'Shadow Map' if is_day else 'Brightness Map'}</b>
    </div>
    """
    m.get_root().html.add_child(folium.Element(info_text))

    if is_day:
        print("Computing shadows for 2000 buildings...")
        buildings_path = os.path.join(DATA, "buildings", "buildings_sample.geojson")
        shadows, alt, az = compute_all_shadows(buildings_path, target_time)
        print(f"Generated {len(shadows)} shadow polygons")

        with open(buildings_path) as f:
            buildings = json.load(f)

        folium.GeoJson(
            buildings,
            style_function=lambda x: {
                "fillColor": "#64748b",
                "color": "#475569",
                "weight": 0.5,
                "fillOpacity": 0.6,
            },
            name="Buildings",
        ).add_to(m)

        shadow_collection = {
            "type": "FeatureCollection",
            "features": shadows
        }
        folium.GeoJson(
            shadow_collection,
            style_function=lambda x: {
                "fillColor": "#1e293b",
                "color": "none",
                "fillOpacity": 0.4,
            },
            name="Shadows",
        ).add_to(m)

    else:
        print("Loading streetlights...")
        lights = load_streetlights()
        print(f"Loaded {len(lights)} streetlights")

        HeatMap(
            lights,
            radius=12,
            blur=20,
            gradient={0.2: "#1e3a5f", 0.4: "#2563eb", 0.6: "#60a5fa", 0.8: "#fbbf24", 1.0: "#ffffff"},
            name="Streetlight Brightness",
        ).add_to(m)

        print("Loading food establishments...")
        places = load_food_establishments()
        print(f"Loaded {len(places)} establishments")

        fg = folium.FeatureGroup(name="Open Businesses")
        for p in places:
            folium.CircleMarker(
                location=[p["lat"], p["lon"]],
                radius=3,
                color="#fbbf24",
                fill=True,
                fillOpacity=0.7,
                popup=p["name"],
            ).add_to(fg)
        fg.add_to(m)

    folium.LayerControl().add_to(m)

    m.save(OUT)
    print(f"\nSaved to {OUT}")
    print("Open in browser to view.")


if __name__ == "__main__":
    import argparse
    from zoneinfo import ZoneInfo

    parser = argparse.ArgumentParser(description="LightMap Boston Prototype")
    parser.add_argument("--time", help="Target time, e.g. '2026-07-15 14:00'")
    parser.add_argument("--night", action="store_true", help="Force night mode (22:00)")
    args = parser.parse_args()

    tz = ZoneInfo("US/Eastern")

    if args.night:
        t = datetime(2026, 7, 15, 22, 0, tzinfo=tz)
    elif args.time:
        t = datetime.strptime(args.time, "%Y-%m-%d %H:%M").replace(tzinfo=tz)
    else:
        t = datetime(2026, 7, 15, 14, 0, tzinfo=tz)

    build_map(t)
