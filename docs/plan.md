# Project Plan: LightMap Boston

> *In the light of day, we shield you from the sun. In the dark of night, we guide you to the light.*

## Summary

A map that shows **where shade is during the day** and **where light is at night** in Boston and Cambridge, updated in real time based on sun position, building geometry, streetlights, and weather.

**Scope:** City of Boston and City of Cambridge.

---

## Problem

People walk, run, and move through the city every day. But they don't know:

- Where is shaded right now? (hot afternoon, high UV)
- Where is well-lit right now? (dark evening, walking home)
- Where tends to flood when it rains?
- Where tends to ice over in winter?

This information exists in public data, but nobody has put it on a single map. Existing tools (ShadeMap, Shadowmap.org) cover only daytime shadows and lack nighttime lighting, weather hazards, or Boston-specific focus.

---

## What We Build

An interactive map of Boston and Cambridge that visualizes:

| Time / Condition | What the map shows |
|------------------|-------------------|
| Daytime | Shaded areas based on sun angle + building height + tree canopy |
| Nighttime | Bright areas based on 80K+ streetlight locations + open businesses |
| Rain | Historically flood-prone areas (5,700+ 311 complaints) |
| Below freezing | Historically icy areas (42K+ 311 complaints) |

The map auto-switches between day and night mode based on the time slider. Users look at the map and make their own decisions.

**Key interactions:**
- Time slider (30-min steps, full 24h range) to watch shadows move or explore nighttime
- Click anywhere for contextual details (building height, shadow length, brightness level)
- Toggle layers independently (shadows, buildings, trees, streetlights, businesses, crime, flood, ice)
- Real-time weather panel (temperature, UV, AQI, rain/snow alerts)
- Onboarding overlay for first-time users

---

## Competitive Landscape

No existing product combines daytime shade + nighttime brightness + weather hazards on one map. See `docs/competitive-research.md` for detailed analysis.

| Feature | ShadeMap | Shadowmap.org | Safest Way | LightMap Boston |
|---------|----------|---------------|------------|-----------------|
| Daytime shadow | Yes | Yes | - | Yes |
| Nighttime brightness | - | - | Yes (routes) | Yes (visualization) |
| Weather hazards | - | - | - | Yes (flood + ice) |
| Boston-specific | - | - | - | Yes |
| Free, no login | Partial | Partial (today only) | Yes | Yes |

**Design references from competitors:**
- **Shadowmap.org:** Time slider at bottom + 24h animation is an intuitive UX pattern. Sun path visualization and seasonal presets (solstice/equinox buttons) are useful for power users. Time-integrated shadow accumulation (LBS 2019 paper) is a potential future enhancement.
- **ShadeMap:** Click-to-inspect for sun hours per pixel. Heatmap color ramp (dark → blue → green → red) for sun exposure density.
- **Safest Way:** Lighting level per road segment ("fully lit" = lamp every 30m) — inspired our click-to-inspect brightness level classification (well-lit / moderately lit / dimly lit / dark).
- **Light Pollution Map:** Overlay opacity control (default 60%) — critical for readability over base map. Color-blind-friendly alternatives.
- **First Street:** 1-10 risk score is brilliantly simple — informed our decision to keep hazard display as heatmaps rather than numeric scores.

---

## Data Sources

### Static Data (downloaded 2026-04-01)

| Data | Records | Source | Purpose |
|------|---------|--------|---------|
| Buildings with height | 46,386 (Boston 28K + Cambridge 18K) | BPDA, Cambridge GIS | Shadow projection |
| Streetlight locations | 80,182 (Boston 74K + Cambridge 6K) | data.boston.gov, Cambridge GIS | Nighttime brightness |
| Tree canopy polygons | 138,099 (Boston 102K + Cambridge 36K) | data.boston.gov, Cambridge GIS | Daytime tree shade |
| Crime incidents | 366K+ (Boston 257K + Cambridge 109K) | data.boston.gov, data.cambridgema.gov | Nighttime safety context |
| Crash records | 59K (Boston 43K + Cambridge 16K) | Vision Zero, data.cambridgema.gov | Nighttime safety context |
| Food establishments | 3,198 | data.boston.gov | Nighttime activity (open businesses) |
| Flood complaints (311) | 5,708 (Boston 3.5K + Cambridge 2.2K) | 311 service requests | Flood risk overlay |
| Ice complaints (311) | 42,283 (Boston 28.6K + Cambridge 13.7K) | 311 service requests | Ice risk overlay |

### Real-Time Data (API, free, no auth)

| Data | Source |
|------|--------|
| UV index + temperature + humidity | Open-Meteo Forecast API |
| Air quality (AQI, PM2.5) | Open-Meteo Air Quality API |
| Weather conditions (rain/snow code) | Open-Meteo (WMO weather codes) |

### Data Limitations

| Data | Issue |
|------|-------|
| Building heights | Boston 2010 survey, Cambridge 2018 flyover. New construction not reflected. |
| Tree canopy | Boston 2019, Cambridge 2018. Trees may have been added or removed. |
| Flood/ice risk | Pattern-based from 311 complaints (2019-2024), not real-time prediction. |
| Shadow geometry | Simplified 2D extrusion. Actual shadows may differ from complex roof shapes. |

---

## System Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Browser (Client)                  │
│  ┌─────────────┐  ┌──────────┐  ┌────────────────┐  │
│  │ MapLibre GL  │  │  Time    │  │  Weather Panel │  │
│  │ JS (map +   │  │  Slider  │  │  (UV, AQI,     │  │
│  │  layers)    │  │  (24h)   │  │   alerts)      │  │
│  └──────┬──────┘  └────┬─────┘  └───────┬────────┘  │
│         │              │                │            │
│         └──────────────┼────────────────┘            │
│                        │ fetch(/api/*)               │
└────────────────────────┼─────────────────────────────┘
                         │
┌────────────────────────┼─────────────────────────────┐
│                  FastAPI Server                       │
│  ┌─────────────┐  ┌────┴─────┐  ┌────────────────┐  │
│  │ /api/shadows │  │/api/info │  │ /api/weather   │  │
│  │ (pvlib +    │  │(sun pos) │  │ (Open-Meteo    │  │
│  │  Shapely)   │  │          │  │  proxy, 5min   │  │
│  │  [cached    │  └──────────┘  │  cache)        │  │
│  │   per 30m]  │                └────────────────┘  │
│  └─────────────┘                                     │
│  ┌─────────────┐  ┌──────────┐  ┌────────────────┐  │
│  │/api/buildings│  │/api/     │  │/api/hazards/   │  │
│  │/api/canopy  │  │streetligh│  │  flood, ice    │  │
│  │  [GeoJSON,  │  │ts [coord │  │/api/safety/    │  │
│  │   cached]   │  │  array]  │  │  nighttime     │  │
│  └─────────────┘  └──────────┘  └────────────────┘  │
│                        │                             │
│              ┌─────────┴──────────┐                  │
│              │  data/ (GeoJSON,   │                  │
│              │  CSV, TopoJSON)    │                  │
│              └────────────────────┘                  │
└──────────────────────────────────────────────────────┘
```

**Key design decisions:**
- **Server-side shadow computation:** Shadows are computed by the Python backend (pvlib + Shapely), not in-browser WebGL. This trades real-time interactivity for simpler frontend code and consistent results. Cached per 30-minute interval (up to 48 slots).
- **Streetlights as coordinate array:** 80K points sent as `[[lon, lat], ...]` instead of GeoJSON to reduce payload size (~60% smaller).
- **Style switching for day/night:** MapLibre base map switches between CARTO Positron (day) and Dark Matter (night) to reinforce the mode visually.

---

## Core Computation

### 1. Shadow Map (daytime)
- Sun position from date + time + latitude using **pvlib** (NREL Solar Position Algorithm)
- Each building: `height × tan(90° - sun_altitude)` = shadow length, projected along sun azimuth
- Shadow polygon = union of building footprint and projected shadow footprint (Shapely `unary_union`)
- Tree canopy polygons add additional shade zones (heatmap layer)
- Shadow length capped at 500m to avoid degenerate polygons at very low sun angles
- Result: GeoJSON overlay showing shaded vs sun-exposed areas

Verified: July 2pm, a 10m building casts a 4.8m shadow. January 2pm, the same building casts a 27m shadow. Seasonal effect is dramatic.

*Reference: Shadowmap.org uses GPU Shadow Mapping with Cascaded Shadow Maps in Three.js for true 3D rendering. Our approach uses 2D geometric projection, which is simpler but sufficient for a top-down map view.*

### 2. Brightness Map (nighttime)
- 80K+ streetlight locations rendered as a heatmap (MapLibre `heatmap` layer)
- Heatmap color ramp: dark → navy → blue → yellow → white (density-based)
- Open businesses marked as orange circles (3K+ food establishments)
- Nighttime crime/crash density as toggleable safety context layer
- Click-to-inspect: counts streetlights within ~200m radius, classifies as well-lit / moderately lit / dimly lit / dark
- Result: visual brightness overlay showing lit vs dark areas

*Reference: Safest Way classifies roads as "fully lit" (lamp post every 30m). Our radius-based approach is less precise per-road but works at map scale without road-network data.*

### 3. Weather Hazard Overlay
- **Rain detected:** Historical flood complaint density shown as blue heatmap (5,700+ data points)
- **Below freezing:** Historical icing complaint density shown as purple heatmap (42K+ data points)
- Weather conditions fetched from Open-Meteo every 5 minutes (WMO weather codes for rain/snow detection)
- Weather panel shows: temperature, UV index (day only), AQI, rain/snow alert

---

## Honest Uncertainty

The system shows what it knows and admits what it does not:

| Situation | Display |
|-----------|---------|
| Building data available | Shade area rendered with confidence |
| Tree data from 2018-2019 | Label: "Tree info may be outdated" |
| No streetlight data for area | Label: "Brightness unknown" |
| Sparse flood history | Label: "Flood risk uncertain" |
| Unprecedented weather | Label: "Beyond historical patterns" |

About panel discloses all data sources, record counts, data periods, and known limitations.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12, FastAPI, uvicorn |
| Shadow computation | pvlib (sun position), Shapely + GeoPandas (geometry) |
| Frontend map | MapLibre GL JS 4.7.1 |
| Base tiles | CARTO Positron (day), CARTO Dark Matter (night) |
| Weather API | Open-Meteo (forecast + air quality, free, no auth) |
| HTTP client | httpx (async-capable, backend weather fetching) |
| Data formats | GeoJSON, CSV, TopoJSON |

---

## Project Structure

```
1001-project/
├── docs/
│   ├── plan.md                  <- this document
│   ├── competitive-research.md  <- competitor analysis (ShadeMap, Shadowmap, etc.)
│   ├── data-catalog.md          <- full data source documentation
│   ├── review-personas.md       <- grading evaluation personas
│   └── specs/mit-gdc/           <- course assignment requirements
├── src/
│   ├── server.py                <- FastAPI backend (all API endpoints)
│   ├── shadow/
│   │   └── compute.py           <- shadow computation engine (pvlib + Shapely)
│   ├── static/
│   │   ├── index.html           <- single-page frontend
│   │   ├── app.js               <- map logic, layers, UI interactions
│   │   └── style.css            <- responsive styling, day/night themes
│   ├── brightness/              <- (data preprocessing)
│   └── weather/                 <- (data preprocessing)
├── data/
│   ├── buildings/               <- Boston building footprints + all_buildings.geojson
│   ├── streetlights/            <- Boston streetlight CSV
│   ├── trees/                   <- Boston canopy + centroids
│   ├── safety/                  <- crime, crash, food establishment data
│   ├── weather/                 <- Boston flood/ice 311 complaints
│   └── cambridge/               <- Cambridge buildings, streetlights, trees, safety, weather
├── requirements.txt
└── README.md
```

---

## Implementation Phases

### Phase 1: Data Collection and Preprocessing [COMPLETE]
- [x] Download and parse building height data (Boston + Cambridge)
- [x] Download streetlight location data (Boston + Cambridge)
- [x] Download tree canopy data (Boston + Cambridge)
- [x] Preprocess crime/crash data by time of day
- [x] Merge Boston + Cambridge datasets into unified GeoJSON

### Phase 2: Core Computation [COMPLETE]
- [x] Sun position calculator (pvlib)
- [x] Building shadow projection (Shapely geometric extrusion)
- [x] Shadow map generation for any given time (cached per 30-min interval)
- [x] Streetlight brightness heatmap
- [x] Weather hazard overlay (flood + ice from 311 data)

### Phase 3: Map Interface [COMPLETE]
- [x] Web map with shadow overlay (daytime, CARTO Positron)
- [x] Web map with brightness overlay (nighttime, CARTO Dark Matter)
- [x] Auto-switch between day/night based on time slider
- [x] Weather condition panel (temperature, UV, AQI, rain/snow alerts)
- [x] Layer toggles (shadows, buildings, trees, streetlights, businesses, crime, flood, ice)
- [x] Click-to-inspect (building height, shadow length, brightness level, business names)
- [x] Onboarding overlay for first-time users
- [x] About panel with data sources and limitations
- [x] Tree canopy heatmap layer

### Phase 4: Polish [COMPLETE]
- [x] Shadow cache (48-slot LRU, 30-min interval keys)
- [x] Streetlight payload optimization (coordinate array vs GeoJSON)
- [x] Day/night visual theme switching
- [x] Hazard layer persistence across mode switches
- [x] Loading indicators and error toasts

### Phase 5: Video Production
- [ ] Proposal video
- [ ] Midpoint video
- [ ] Final video

---

## Grading Alignment

| Criteria (points) | How this project addresses it |
|--------------------|-------------------------------|
| Complexity (15) | Shadow computation from 46K buildings using pvlib + Shapely. Real-time weather integration via Open-Meteo. Day/night mode switching with distinct data pipelines and visual themes. |
| User Interface (15) | Full-screen MapLibre map with time slider, layer toggles, click-to-inspect popups, weather panel, onboarding overlay, About panel. Day/night theme adaptation. Responsive controls. |
| Effort (15) | 10+ data sources across two cities. Custom shadow engine. Full-stack app (FastAPI + MapLibre). Competitive research of 6+ existing tools. Data preprocessing pipeline for 500K+ records. |
| Design (15) | Modular backend (shadow computation separated from API serving). Caching strategy (shadow cache, weather cache, streetlight cache). Honest uncertainty display. Clean separation of day/night layer logic. |
| Video (40) | Live demo: "watch the shadows move as time changes." Day → night transition. Click-to-inspect. Weather alerts triggering hazard overlays. |
| Bonus (10+) | Real-time weather adaptation. Seasonal shadow variation. Data honesty / uncertainty display. Two-city scope (Boston + Cambridge). Onboarding UX. |
