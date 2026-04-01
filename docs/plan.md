# Project Plan: Boston Urban Mapping

> *In the light of day, we shield you from the sun. In the dark of night, we guide you to the light.*

## Summary

A map that shows **where shade is during the day** and **where light is at night** in Boston, updated in real time based on sun position, building geometry, streetlights, and weather.

**Scope:** City of Boston only. Cambridge and other municipalities are out of scope (future work).

---

## Problem

People walk, run, and move through the city every day. But they don't know:

- Where is shaded right now? (hot afternoon, high UV)
- Where is well-lit right now? (dark evening, walking home)
- Where tends to flood when it rains?
- Where tends to ice over in winter?

This information exists in public data, but nobody has put it on a map.

---

## What We Build

An interactive map of Boston that visualizes:

| Time / Condition | What the map shows |
|------------------|-------------------|
| Daytime | Shaded areas based on sun angle + building height + tree canopy |
| Nighttime | Bright areas based on streetlight locations + active businesses |
| Rain | Historically flood-prone areas |
| Below freezing | Historically icy areas |

The map updates automatically as time and weather change. Users look at the map and make their own decisions.

---

## Data Sources

### Static Data (download once)

| Data | Source | Purpose |
|------|--------|---------|
| 3D buildings with height (128K) | BPDA, data.boston.gov | Shadow projection |
| Streetlight locations (74K) | data.boston.gov | Nighttime brightness |
| Tree canopy polygons | data.boston.gov | Daytime tree shade |
| Crime incidents with hour (257K+) | data.boston.gov | Nighttime safety context |
| Crash records with timestamp (42K+) | Vision Zero, data.boston.gov | Nighttime safety context |
| Food establishment locations | data.boston.gov | Nighttime activity (open businesses) |

### Real-Time Data (API, free, no auth)

| Data | Source |
|------|--------|
| UV index + temperature | Open-Meteo |
| Air quality (AQI) | Open-Meteo |
| Weather conditions (rain/snow) | NWS API |

### Indirect Estimation

| Data | Source | Limitation |
|------|--------|------------|
| Flood-prone areas | Historical 311 flooding complaints | Pattern-based, not real-time |
| Icy areas | Historical 311 icing complaints | Pattern-based, not real-time |
| Business hours | Google Places API | Paid ($200/mo free credit) |

---

## Core Computation

### 1. Shadow Map (daytime)
- Sun position from date + time + latitude (pvlib library)
- Each building: height x tan(90 - sun altitude) = shadow length, projected along sun azimuth
- Tree canopy polygons add additional shade zones
- Result: overlay on map showing shaded vs sun-exposed areas

Verified: July 2pm, a 10m building casts a 4.8m shadow. January 2pm, the same building casts a 27m shadow. Seasonal effect is dramatic.

### 2. Brightness Map (nighttime)
- Streetlight locations plotted with proximity glow
- Active businesses marked (location + hours if available)
- Historical nighttime crime/crash density as safety context layer
- Result: overlay on map showing bright/active vs dark/quiet areas

### 3. Weather Hazard Overlay
- Rain: historical flood complaint density shown when precipitation detected
- Winter: historical icing complaint density shown when temperature is below freezing

---

## Honest Uncertainty

The system shows what it knows and admits what it does not:

| Situation | Display |
|-----------|---------|
| Building data available | Shade area rendered with confidence |
| Tree data from 2019 | Label: "Tree info may be outdated" |
| No streetlight data for area | Label: "Brightness unknown" |
| Sparse flood history | Label: "Flood risk uncertain" |
| Unprecedented weather | Label: "Beyond historical patterns" |

---

## Project Structure

```
1001-project/
├── docs/
│   ├── plan.md              <- this document
│   └── specs/               <- course requirements
├── src/
│   ├── shadow/              <- shadow computation module
│   ├── brightness/          <- nighttime brightness module
│   └── weather/             <- real-time weather/UV/AQI + hazard overlay
├── data/
│   ├── buildings/           <- 3D building data
│   ├── streetlights/        <- streetlight locations
│   ├── trees/               <- tree canopy
│   └── safety/              <- crime/crash data
└── README.md
```

---

## Implementation Phases

### Phase 1: Data Collection and Preprocessing
- [ ] Download and parse building height data
- [ ] Download streetlight location data
- [ ] Download tree canopy data
- [ ] Preprocess crime/crash data by time of day

### Phase 2: Core Computation
- [ ] Sun position calculator
- [ ] Building shadow projection
- [ ] Shadow map generation for any given time
- [ ] Streetlight brightness map
- [ ] Weather hazard overlay

### Phase 3: Map Interface
- [ ] Web map with shadow overlay (daytime)
- [ ] Web map with brightness overlay (nighttime)
- [ ] Auto-switch between day/night based on time
- [ ] Weather condition panel (current UV, temperature, AQI)
- [ ] Honest uncertainty labels

### Phase 4: Video Production
- [ ] Proposal video
- [ ] Midpoint video
- [ ] Final video

---

## Tech Stack (planned)

- Python 3.12
- pvlib (sun position)
- Shapely / GeoPandas (spatial operations, shadow geometry)
- FastAPI or Flask (backend)
- Leaflet or Mapbox (frontend map)
- Open-Meteo API (weather/UV/AQI)

---

## Grading Alignment

| Criteria (points) | How this project addresses it |
|--------------------|-------------------------------|
| Complexity (15) | 3D shadow computation from 128K buildings + real-time weather integration |
| User Interface (15) | Interactive map with time-adaptive overlays and condition panel |
| Effort (15) | Multi-source data integration, shadow engine, full stack |
| Design (15) | Modular architecture, honest uncertainty display |
| Video (40) | Live demo: "watch the shadows move as time changes" |
| Bonus (10+) | Real-time adaptation + seasonal variation + data honesty |
