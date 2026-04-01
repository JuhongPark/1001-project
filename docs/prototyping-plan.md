# Prototyping Plan: LightMap Boston

## Current State

Working prototype (`src/prototype.py`) generates a static HTML map using folium.
- Daytime: shadow polygons from 2,000 sample buildings
- Nighttime: streetlight heatmap (74K) + food establishment markers (3.2K)
- No interactivity (no time slider, no layer toggles, no real-time weather)

---

## Tech Stack

| Layer | Tool | Why |
|-------|------|-----|
| Backend | **FastAPI** | Lightweight Python API, async support, easy to serve precomputed data |
| Frontend map | **Mapbox GL JS** | WebGL rendering handles 128K buildings smoothly, built-in day/night styles |
| Shadow computation | **pvlib + Shapely** (existing) | Already working, keep as-is |
| Spatial data | **GeoPandas** | Efficient bulk processing of shapefiles and GeoJSON |
| Real-time weather | **Open-Meteo API + NWS API** | Free, no auth, already documented in data catalog |
| Frontend UI | **Vanilla JS + HTML/CSS** | No framework overhead for a single-page map app |
| Data format | **GeoJSON + Tippecanoe → MBTiles** | Vector tiles for large datasets (128K buildings) |
| Dev server | **uvicorn** | ASGI server for FastAPI |

### Why not keep folium?
- folium generates static HTML — cannot update shadows without regenerating the whole page
- Cannot handle 128K buildings in-browser (GeoJSON too large)
- No time slider or real-time interaction possible

### Why Mapbox GL JS over Leaflet?
- WebGL rendering: Leaflet chokes on 128K polygons, Mapbox GL handles it natively
- Built-in vector tile support for large datasets
- Built-in dark/light style switching for day/night modes
- Free tier (50K map loads/month) is more than enough for a course project

---

## Prototype Phases

### Phase 1: Static API + Map Shell

**Goal:** Replace folium with a proper web map that loads data from a backend.

**Tasks:**
- [ ] Set up FastAPI with a single endpoint: `GET /api/shadows?time=2026-07-15T14:00`
- [ ] Precompute shadow GeoJSON for a given time and return it
- [ ] Create `index.html` with Mapbox GL JS showing Boston
- [ ] Load and render shadow polygons from the API on the map
- [ ] Load streetlight data as a heatmap layer
- [ ] Auto-switch base style: light (day) / dark (night) based on sun altitude

**Output:** Interactive map with API-driven shadow/brightness rendering.

### Phase 2: Time Slider + Day/Night Transition

**Goal:** User can drag a slider to see shadows move throughout the day.

**Tasks:**
- [ ] Add a time slider UI (24-hour range for a selected date)
- [ ] On slider change, fetch new shadow data from API
- [ ] Smooth transition between day/night base map styles at sunrise/sunset
- [ ] Info panel showing current time, sun position, mode
- [ ] Precompute shadow snapshots at 30-min intervals for performance (cache)

**Output:** "Watch the shadows move" — the key demo moment for the video.

### Phase 3: Weather + Hazard Overlays

**Goal:** Add real-time weather context and historical hazard layers.

**Tasks:**
- [ ] Integrate Open-Meteo API: current UV index, temperature, AQI
- [ ] Integrate NWS API: current weather conditions (rain/snow)
- [ ] Weather info panel on the map
- [ ] Load historical flood complaint density → show when rain detected
- [ ] Load historical ice complaint density → show when below freezing
- [ ] Layer toggle controls for each overlay

**Output:** Map responds to real weather conditions with relevant hazard overlays.

### Phase 4: Full Data + Performance

**Goal:** Scale from 2K sample to 128K buildings, add tree canopy.

**Tasks:**
- [ ] Process full 128K building dataset with GeoPandas
- [ ] Generate vector tiles (Tippecanoe) for buildings + shadows
- [ ] Add tree canopy polygons as additional shade layer
- [ ] Add crime/crash density as nighttime safety context layer
- [ ] Performance target: shadow update < 2 seconds for full dataset
- [ ] Honest uncertainty labels for data gaps

**Output:** Production-quality map with complete Boston coverage.

### Phase 5: Polish + Video

**Goal:** Final visual polish and video-ready state.

**Tasks:**
- [ ] Unified color system across all overlays
- [ ] Legend design (collapsible, clear)
- [ ] Mobile-responsive layout
- [ ] Loading states and empty state messages
- [ ] "About" panel explaining data sources and limitations
- [ ] Test against all 6 review personas

**Output:** Demo-ready application for final video.

---

### Phase 6: AI Guide Agent (optional, not core)

**Goal:** LLM-powered conversational agent that interprets map data and gives practical advice.

**What it does:**
- Reads current map state (time, weather, active overlays) and gives natural language insights
- Examples:
  - "It's 90°F and sunny — the shaded areas along Commonwealth Ave would be good for a run."
  - "Heavy rain expected this afternoon. These areas near Back Bay have flooded before."
  - "It's below freezing tonight. Watch out for icy spots around Beacon Hill."
  - "This neighborhood is well-lit with lots of open businesses — looks active tonight."
  - "Almost every low-lying area shows flood history — maybe stay indoors today."

**What it does NOT do:**
- No route computation (no Dijkstra, A*, or pathfinding)
- No turn-by-turn directions
- User still looks at the map and decides their own path

**Architecture consideration:**
- Backend endpoint: `POST /api/guide` with current map context (time, weather, visible layers)
- LLM call (Claude API) with structured prompt containing map data summary
- Response displayed in a chat panel or card overlay on the map
- Keep it stateless: each query is independent, no conversation memory needed

**Tasks:**
- [ ] Define prompt template with map context variables
- [ ] API endpoint that collects current state and calls Claude API
- [ ] UI: chat bubble or insight card on the map
- [ ] Rate limiting / caching to control API costs

**Output:** "Ask the map" feature — user clicks a button, gets a plain-language summary of current conditions and suggestions.

---

## Project Structure (target)

```
1001-project/
├── src/
│   ├── server.py              ← FastAPI app entry point
│   ├── shadow/
│   │   ├── compute.py         ← existing shadow engine
│   │   └── cache.py           ← precomputed shadow snapshots
│   ├── brightness/
│   │   └── compute.py         ← streetlight + business brightness
│   ├── weather/
│   │   └── api.py             ← Open-Meteo + NWS integration
│   ├── guide/
│   │   └── agent.py           ← LLM-based insight agent (optional)
│   └── static/
│       ├── index.html          ← single-page map app
│       ├── style.css
│       └── app.js              ← map logic, time slider, layer controls
├── data/
│   ├── buildings/
│   ├── streetlights/
│   ├── trees/
│   ├── safety/
│   └── weather/
└── docs/
```

---

## Key Dependencies

```
# requirements.txt (additions to existing)
fastapi
uvicorn
geopandas
httpx            # async HTTP for weather APIs
anthropic        # Claude API for AI guide agent (optional)
```

Existing: pvlib, shapely, pandas, folium (keep for quick testing)
