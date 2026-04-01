# Project Plan: Boston Urban Mapping

> *In the light of day, we shield you from the sun. In the dark of night, we guide you to the light.*

## Summary

A map-based system that recommends optimal walking and running routes based on time of day and weather conditions. Shaded and comfortable paths by day, well-lit and active streets by night, and hazard-aware detours in adverse weather.

---

## Problem

"Right now, from here, which way should I walk?"

Existing map apps (Google Maps, Apple Maps) optimize for **shortest distance or fastest time**. But what people actually care about while walking or running:

- Hot summer afternoon: Where is the shade?
- Dark winter evening: Which streets are well-lit and active?
- Rainy day: Which spots tend to flood?
- After a snowstorm: Where are the icy patches?

No app answers these questions.

---

## How It Works

### Input
- Origin and destination
- Current time (automatic)
- Current weather (automatic, via API)

### Processing

Route edge weights change dynamically based on time and conditions:

| Condition | Preferred | Avoided |
|-----------|-----------|---------|
| Summer day (high UV) | Building/tree shadow segments | Sun-exposed segments |
| Night | Streetlight-dense, open-business areas | Dark, isolated segments |
| Rain | Historically low-flood segments | Flood-prone segments |
| Winter (below freezing) | Priority snow-cleared roads | Historically icy segments |

### Output
- Recommended route on an interactive map
- Per-segment condition indicators (shade ratio, streetlight density, hazard warnings)
- Honest uncertainty: "Insufficient data for this segment"

---

## Data Sources

### Static Data (download once)

| Data | Source | Format | Purpose |
|------|--------|--------|---------|
| 3D buildings (with height) | BPDA, data.boston.gov | CSV/GeoJSON | Shadow computation |
| Streetlight locations (74,065) | data.boston.gov | CSV (lat/lon) | Night path brightness |
| Tree canopy | data.boston.gov | GeoJSON/Raster | Tree shade |
| Road network | OpenStreetMap | PBF -> graph | Route search |
| Crime incidents (with hour) | data.boston.gov | CSV (257K+) | Night safety score |
| Crash records (with timestamp) | Vision Zero, data.boston.gov | CSV (42K+) | Intersection risk |
| Food establishment locations | data.boston.gov | CSV (lat/lon) | Night activity |

### Real-Time Data (API calls)

| Data | Source | Auth | Refresh |
|------|--------|------|---------|
| UV index + temperature | Open-Meteo | None | Real-time |
| Air quality (AQI) | Open-Meteo | None | Real-time |
| Weather conditions (rain/snow) | NWS API | None | Hourly |

### Indirect Estimation

| Data | Source | Purpose | Limitation |
|------|--------|---------|------------|
| Flood-prone segments | Historical 311 flooding complaints | Rainy-day avoidance | Not real-time, pattern-based |
| Icy segments | Historical 311 icing complaints | Winter avoidance | Not real-time, pattern-based |
| Business hours | Google Places API | Night activity estimation | Paid ($200/mo free credit) |

---

## Core Computation

### 1. Shadow Calculation (daytime)
- Sun position: date + time + latitude -> altitude + azimuth (via pvlib)
- Building shadow: height x tan(90 - altitude) = shadow length, projected along azimuth
- Tree shadow: canopy polygon radius as approximation
- Per-road-segment shade ratio

### 2. Night Path Score
- Streetlight density: count within 50m buffer of each road segment
- Business activity: number of open businesses nearby (location + hours)
- Safety score: nighttime (20:00-06:00) crime/crash frequency from historical data
- Composite score = weighted sum

### 3. Adverse Weather Risk
- Rain: historical flood complaint density x current precipitation status
- Winter: historical icing complaint density x current sub-zero temperature

### 4. Route Search
- OSM road network -> graph conversion (OSMnx)
- Edge weights = distance + condition-based penalty/bonus
- Dijkstra or A* for optimal path

---

## Answer Downgrade Design

The system is honest about what it does not know:

| Situation | System Response |
|-----------|-----------------|
| Building data available | "72% shade on this segment" (confident) |
| Tree data from 2019 | "Tree info is outdated, may differ from current state" (warning) |
| No streetlight data for segment | "Cannot assess brightness for this segment" (withheld) |
| Sparse flood history | "Insufficient flood history, risk uncertain" (withheld) |
| Unprecedented storm | "Beyond historical patterns, cannot predict" (refused) |

---

## Project Structure

```
1001-project/
├── docs/
│   ├── plan.md              <- this document
│   └── specs/               <- course requirements
├── src/
│   ├── shadow/              <- shadow computation module
│   ├── nightpath/           <- night path scoring module
│   ├── routing/             <- route search engine
│   └── weather/             <- real-time weather/UV/AQI
├── data/
│   ├── buildings/           <- 3D building data
│   ├── streetlights/        <- streetlight locations
│   ├── trees/               <- tree canopy
│   ├── safety/              <- crime/crash data
│   └── weather/             <- weather cache
└── README.md
```

---

## Implementation Phases

### Phase 1: Data Collection and Preprocessing
- [ ] Download and parse building height data
- [ ] Download streetlight location data
- [ ] Download tree canopy data
- [ ] Convert OSM road network to graph
- [ ] Preprocess crime/crash data by time of day

### Phase 2: Core Computation Engine
- [ ] Sun position calculator
- [ ] Building shadow projection engine
- [ ] Per-segment shade ratio calculation
- [ ] Night path scoring (streetlights + businesses + safety)
- [ ] Adverse weather risk scoring

### Phase 3: Route Search
- [ ] Condition-weighted route search
- [ ] Real-time weather API integration
- [ ] Answer downgrade logic

### Phase 4: UI / Map
- [ ] Web map interface
- [ ] Route visualization (color-coded segments)
- [ ] Condition panel (current UV, temperature, AQI)

### Phase 5: Video Production
- [ ] Proposal video
- [ ] Midpoint video
- [ ] Final video

---

## Tech Stack (planned)

- Python 3.12
- pvlib (sun position)
- OSMnx + NetworkX (road graph + routing)
- Shapely / GeoPandas (spatial operations)
- FastAPI or Flask (backend)
- Leaflet or Mapbox (frontend map)
- Open-Meteo API (weather/UV/AQI)

---

## Grading Alignment

| Criteria (points) | How this project addresses it |
|--------------------|-------------------------------|
| Complexity (15) | 3D shadow computation + multi-condition routing + real-time API |
| User Interface (15) | Interactive map, color-coded segments, condition panel |
| Effort (15) | Multi-source data integration, computation engine, full stack |
| Design (15) | Modular architecture, answer downgrade structure |
| Video (40) | "Which path right now?" demo is visually compelling |
| Bonus (10+) | Real-time + seasonal adaptation + honest uncertainty |
