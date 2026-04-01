# LightMap Boston - Data Catalog

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
