# LightMap Boston - Data Catalog

## Download Log

All datasets downloaded on **2026-04-01**.

### Boston (data.boston.gov)

| Dataset | Records | Valid Coords | File | Data Period |
|---------|---------|-------------|------|-------------|
| Buildings with height | 128,608 | 105,121 with height | `data/buildings/buildings.csv` | 2010 survey |
| Buildings sample (GeoJSON) | 2,000 | 2,000 | `data/buildings/buildings_sample.geojson` | Subset of above |
| Streetlight locations | 74,065 | 74,065 (100%) | `data/streetlights/streetlights.csv` | Current as of download |
| Tree canopy polygons | 108,131 | 108,131 | `data/trees/TreeTops2019.geojson` | 2019 baseline, EPSG:2249 (needs reprojection) |
| Crime incidents | 257,030 | 242,056 (94%) | `data/safety/crime_incidents.csv` | 2023-01-01 to 2026-03-29 |
| Crash records | 42,685 | 42,685 (100%) | `data/safety/crash_records.csv` | 2015-01-01 to 2025-12-31 |
| Food establishments | 3,198 | 2,993 (94%) | `data/safety/food_establishments.csv` | Active licenses |
| Flood complaints (311) | 3,486 | 3,483 (99%) | `data/weather/flood_complaints.csv` | 2019-01-01 to 2024-12-31 |
| Ice complaints (311) | 28,631 | 28,623 (99%) | `data/weather/ice_complaints.csv` | 2019-01-02 to 2024-12-30 |

### Cambridge (data.cambridgema.gov, cambridgegis GitHub)

| Dataset | Records | Valid Coords | File | Data Period |
|---------|---------|-------------|------|-------------|
| Buildings with height | 18,234 | 18,234 (WGS84) | `data/cambridge/buildings/buildings.geojson` | 2018 flyover |
| Streetlight locations | 6,117 | 6,117 (WGS84) | `data/cambridge/streetlights/streetlights.geojson` | Current as of 2025-10 |
| Tree canopy polygons | 36,266 | 36,266 (WGS84) | `data/cambridge/trees/tree_canopy_2018.topojson` | 2018, TopoJSON (needs conversion) |
| Crime incidents | 109,214 | 109,209 (~100%) | `data/cambridge/safety/crime_incidents.csv` | 2009-01-01 to 2026-02-28 |
| Crash records | 16,247 | 8,739 (54%) | `data/cambridge/safety/crash_records.csv` | 2015-01-01 to 2026-02-28 |
| Flood complaints (311) | 2,222 | 2,222 (100%) | `data/cambridge/weather/flood_complaints.csv` | 2012-02-02 to 2026-03-27 |
| Ice complaints (311) | 13,652 | 13,652 (100%) | `data/cambridge/weather/ice_complaints.csv` | 2013-02-10 to 2026-03-24 |

---

## Static Data

### 1. Buildings with Height
- **Source:** BPDA, data.boston.gov
- **Dataset:** Boston Buildings with Roof Breaks
- **Records:** 128,608
- **Key fields:** BLDG_HGT_2010 (height in feet), shape_wkt (footprint polygon)
- **Format:** CSV, GeoJSON, Shapefile
- **Download:** https://data.boston.gov/dataset/boston-buildings-with-roof-breaks
- **API resource ID:** 2c683b81-7b88-4add-80ad-765e177092bf
- **Used for:** Shadow projection (daytime)

### 2. Streetlight Locations
- **Source:** data.boston.gov
- **Dataset:** Streetlight Locations
- **Records:** 74,065
- **Key fields:** Lat, Long
- **Format:** CSV, KML, Shapefile
- **Download:** https://data.boston.gov/dataset/streetlight-locations
- **API resource ID:** c2fcc1e3-c38f-44ad-a0cf-e5ea2a6585b5
- **Used for:** Brightness map (nighttime)

### 3. Tree Canopy
- **Source:** data.boston.gov
- **Dataset:** Canopy Change Assessment - 2019 Tree Canopy Polygons
- **Coverage:** Citywide
- **Format:** Shapefile (ZIP)
- **Download:** https://data.boston.gov/dataset/canopy-change-assessment
- **Used for:** Additional shade zones (daytime)

### 4. Crime Incidents
- **Source:** data.boston.gov
- **Dataset:** Crime Incident Reports (August 2015 - To Date)
- **Records:** 257,000+
- **Key fields:** OCCURRED_ON_DATE, HOUR (0-23), Lat, Long
- **Format:** CSV
- **API resource ID:** b973d8cb-eeb2-4e7e-99da-c92938efc9c0
- **Used for:** Nighttime safety context

### 5. Crash Records
- **Source:** Vision Zero, data.boston.gov
- **Dataset:** Vision Zero Crash Records
- **Records:** 42,685
- **Key fields:** dispatch_ts (timestamp), lat, long
- **Format:** CSV
- **API resource ID:** e4bfe397-6bfc-49c5-9367-c879fac7401d
- **Used for:** Nighttime safety context

### 6. Food Establishment Locations
- **Source:** data.boston.gov
- **Dataset:** Active Food Establishment Licenses
- **Records:** ~3,200
- **Key fields:** businessname, address, latitude, longitude
- **Format:** CSV
- **API resource ID:** f1e13724-284d-478c-b8bc-ef042aa5b70b
- **Used for:** Nighttime activity (open businesses)

## Real-Time APIs

### 7. UV Index + Temperature + AQI
- **Source:** Open-Meteo
- **Auth:** None required
- **Endpoint:** https://api.open-meteo.com/v1/forecast?latitude=42.36&longitude=-71.06&current=uv_index,temperature_2m
- **AQI endpoint:** https://air-quality-api.open-meteo.com/v1/air-quality?latitude=42.36&longitude=-71.06&current=us_aqi,pm2_5
- **Used for:** Daytime UV conditions, weather overlay

### 8. Weather Conditions
- **Source:** NWS API
- **Auth:** None required
- **Endpoint:** https://api.weather.gov/stations/KBOS/observations/latest
- **Hourly forecast:** https://api.weather.gov/gridpoints/BOX/71,90/forecast/hourly
- **Used for:** Rain/snow detection, temperature

## Indirect Estimation

### 9. Flood-Prone Areas
- **Source:** Boston 311 Service Requests (historical flooding complaints)
- **Filter:** reason contains "flooding" or "flood"
- **Used for:** Rain overlay
- **Limitation:** Pattern-based, not real-time

### 10. Icy Areas
- **Source:** Boston 311 Service Requests (historical icing complaints)
- **Filter:** reason contains "icy" or "ice" or "slippery"
- **Used for:** Winter overlay
- **Limitation:** Pattern-based, not real-time

## Rain & Snow Data Sources

Verified working on 2026-04-05. All free, no API keys required.

### 11. Rain Radar (Real-time)
- **Source:** RainViewer API
- **Auth:** None required
- **Index endpoint:** `https://api.rainviewer.com/public/weather-maps.json`
- **Tile URL:** `https://tilecache.rainviewer.com{path}/256/{z}/{x}/{y}/2/1_1.png`
- **Format:** XYZ raster tiles (256x256 PNG, transparent background)
- **Coverage:** Global composite radar
- **Update frequency:** Every 10 minutes, returns ~13 past frames (~2 hours of history)
- **Used for:** Real-time precipitation overlay on map
- **Limitation:** Nowcast frames intermittently available. No historical lookback beyond ~2 hours.

### 12. Rain Radar Backup (Real-time)
- **Source:** Iowa Environmental Mesonet (IEM) NEXRAD
- **Auth:** None required
- **Tile URL:** `https://mesonet.agron.iastate.edu/cache/tile.py/1.0.0/nexrad-n0q-900913/{z}/{x}/{y}.png`
- **Format:** XYZ raster tiles (256x256 RGBA PNG)
- **Coverage:** Continental US (NWS base reflectivity)
- **Update frequency:** Real-time, always returns latest composite
- **Used for:** Fallback if RainViewer is unavailable
- **Note:** Static URL, no API call needed to get tile path

### 13. Precipitation Forecast (Hourly)
- **Source:** Open-Meteo Forecast API (same base as #7)
- **Auth:** None required
- **Endpoint:** `https://api.open-meteo.com/v1/forecast?latitude=42.36&longitude=-71.06&hourly=precipitation_probability,precipitation,rain,snowfall,weather_code&forecast_days=2`
- **Format:** JSON
- **Fields:** `precipitation_probability` (%), `precipitation` (mm), `rain` (mm), `snowfall` (cm), `weather_code` (WMO)
- **Coverage:** 48 hours of hourly data
- **Update frequency:** Every 1-3 hours
- **Used for:** "Rain in 2 hours" forecast timeline
- **Verified:** 48 data points returned, 7/48 hours showed precipitation > 0 in test

### 14. FEMA Flood Zones (Metro Boston)
- **Source:** FEMA via Boston ArcGIS
- **Auth:** None required
- **Endpoint:** `https://services.arcgis.com/sFnw0xNflSi8J0uh/arcgis/rest/services/FEMA_2009_DFIRM_100YR_500YR_Clipped_Flood_Zones_Metro_Boston/FeatureServer/0/query?where=1=1&outFields=*&f=geojson`
- **Format:** GeoJSON (Polygon)
- **Key fields:** `FLD_ZONE` (AE, X, etc.), `Flood_Zone` (100 YR Flood Zone, 500 YR Flood Zone)
- **Coverage:** Metro Boston (100-year and 500-year flood zones)
- **Used for:** Authoritative flood zone polygon overlay
- **Note:** Must include `outFields=*` or properties return null

### 15. Climate Ready Boston Sea Level Rise Inundation
- **Source:** City of Boston via ArcGIS
- **Auth:** None required
- **Endpoint:** `https://services.arcgis.com/sFnw0xNflSi8J0uh/arcgis/rest/services/Climate_Ready_Boston_Sea_Level_Rise_Inundation/FeatureServer/{layer}/query?where=1=1&outFields=*&f=geojson`
- **Format:** GeoJSON (MultiPolygon)
- **Layers:** 0-8 representing different scenarios:
  - Layer 0: 21" SLR, 10% annual flood
  - Layer 1: 21" SLR, 1% annual flood
  - Layer 2: 21" SLR, high tide
  - Layer 6: 9" SLR, 10% annual flood (near-term, recommended)
  - Layer 7: 9" SLR, 1% annual flood
  - Layer 8: 9" SLR, high tide
- **Used for:** Sea level rise flood scenario overlay
- **Note:** Properties contain only `Shape_Leng` and `Shape_Area`; scenario info is encoded in layer index

### WMO Weather Codes (Rain/Snow)

| Code | Condition | Map Action |
|------|-----------|------------|
| 51/53/55 | Drizzle (light/moderate/dense) | Rain indicator |
| 61/63/65 | Rain (slight/moderate/heavy) | Rain indicator + radar |
| 66/67 | Freezing rain | Rain + ice warning |
| 71/73/75 | Snowfall (slight/moderate/heavy) | Snow indicator |
| 77 | Snow grains | Snow indicator |
| 80-82 | Rain showers | Rain indicator + radar |
| 85/86 | Snow showers | Snow indicator |
| 95/96/99 | Thunderstorm | Rain indicator + radar + alert |

## 311 Complaint Data Verification (2026-04-05)

| File | Records | Valid Coords | Out-of-bounds |
|------|---------|-------------|---------------|
| Boston flood complaints | 3,486 | 3,483 (99.9%) | 3 |
| Boston ice complaints | 28,631 | 28,623 (99.97%) | 8 |
| Cambridge flood complaints | 2,222 | 2,222 (100%) | 0 |
| Cambridge ice complaints | 13,652 | 13,652 (100%) | 0 |
| **Total** | **47,991** | **47,980** | **11** |

Coordinate ranges: lat 42.23-42.40, lon -71.19 to -70.97 (within Boston/Cambridge bounds).
