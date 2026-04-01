# Competitive Research: LightMap Boston

## Shade / Shadow Map Tools

### ShadeMap (shademap.app)
- **What:** Real-time shadow simulation from buildings, trees, terrain. Global coverage.
- **Tech:** Mapbox GL JS, WebGL, OSM data. Open-source npm packages (`mapbox-gl-shadow-simulator`).
- **Pricing:** Free tier for education. Paid commercial/enterprise.
- **Similarity:** Closest competitor for daytime layer. No nighttime or weather layers.

**UI/UX Analysis:**
- Full-screen map, controls distributed around edges (time at top-center, layers bottom-right)
- Shadow color: grey (user-selectable). Sun hours heatmap: black → blue → green → red
- Time control: unconventional inverted slider (drag background, not pointer) — confusing for new users
- Click any pixel to see exact sun hours value
- Shadows only compute from viewport data — must zoom out for broader coverage
- No onboarding tutorial
- **Strengths:** Clean, fast, real-time WebGL rendering. Heatmap views are powerful.
- **Weaknesses:** Inverted time slider is unintuitive. Viewport-only rendering is confusing.

### Shadowmap (shadowmap.org)
- **What:** 3D sunlight visualization with Google 3D Buildings. Targets architects, solar professionals.
- **Tech:** Three.js, 3D rendering, Draco compression.
- **Pricing:** Freemium. Free restricts to today's date.
- **Similarity:** Professional 3D shadow tool. No nighttime or weather layers.

**UI/UX Analysis:**
- Full-screen 3D map with full camera freedom (tilt to ground level)
- Time slider at bottom with "24H" animation button
- Realistic ambient lighting adjusts automatically (dawn/dusk vs noon)
- Left-click buildings to adjust height/visibility
- **Strengths:** True 3D is visually impressive. 24-hour animation is useful.
- **Weaknesses:** Controls take too much screen space ("clunky and outdated" per reviews). Not collapsible without paid subscription. Mobile rendering quality inconsistent.

---

## Nighttime Brightness / Safety Maps

### Safest Way (safestway.co.uk)
- **What:** AI-powered nighttime walking safety app. Safety-scores streets using streetlights, CCTV, crime data.
- **Tech:** OpenAI CLIP for perceived safety, 500K+ streetlights via FOI. AWS hosted.
- **Pricing:** Free (beta). London/Derry/York only.
- **Origin:** UCL PhD project. ~1,000 users.
- **Similarity:** Closest competitor for nighttime layer. But route recommendation, not visualization.

**UI/UX Analysis:**
- Mobile-first design. Dark blue (#17141F) + gold/tan (#E8CCB0) palette
- London Lighting Map: full-screen, every road segment color-coded by lighting level
- "Fully lit" = lamp post every 30 meters
- Value proposition immediately clear: "find the safest, brightest walking routes"
- Safety layers (crime, lighting, CCTV) baked into combined score, not individually toggleable
- **Strengths:** Clear focused value proposition. Award-winning lighting map visualization (UCL first prize).
- **Weaknesses:** Very limited coverage (3 cities). Cannot toggle individual safety layers.

### Light Pollution Map (lightpollutionmap.info)
- **What:** Global artificial sky brightness from NASA VIIRS satellite data + Bortle scale.
- **Tech:** NASA Black Marble satellite imagery.
- **Pricing:** Free web. Paid mobile app (no ads, offline mode).
- **Similarity:** Macro-scale nighttime light — not street-level.

**UI/UX Analysis:**
- Full-screen map with collapsible right-side menu
- Bortle Scale colors: dark blue (dark skies) → green → yellow → red/white (urban)
- Overlay opacity slider (default 60%) — critical for readability over base map
- Color-blind-friendly alternative colors available
- Click shows popup with coordinates, VIIRS value, elevation
- Draw polygon to get aggregate statistics within area
- Dark mode toggle for website theme
- Year-by-year satellite data selection (2012-2023)
- **Strengths:** Opacity control, color-blind option, polygon statistics tool, dark mode.
- **Weaknesses:** Scientific units (nW/cm2/sr) alienate casual users. No onboarding.

---

## Urban Weather Hazard Maps

### First Street / Flood Factor (firststreet.org)
- **What:** Flood risk scores (1-10) for 142M U.S. properties. 30-year climate forecast.
- **Tech:** Mapbox GL JS, proprietary flood model. Integrated into Zillow.
- **Pricing:** Free property lookups. Paid enterprise data licensing.
- **Similarity:** Flood hazard data model. Property-focused, not pedestrian.

**UI/UX Analysis:**
- Address-search-first interface (prominent search bar on homepage)
- Score 1-10 at top-left of every property page — instant risk comprehension
- Color-coded dots on zoomed-out map (green → yellow → red)
- Blue shading for flood depth on inundation maps
- Dual map approach: static "snapshot" maps (instant load) + dynamic Mapbox maps (interactive)
- Three map types per property: Current/Future, Historic, Community
- **Strengths:** 1-10 score is brilliantly simple. Address-search matches user mental model.
- **Weaknesses:** No map legend (explicitly criticized). Cannot click map pins for info (must re-enter address). 40% address lookup failure rate reported.

### Climate Ready Boston (boston.gov)
- **What:** Boston-specific flooding scenarios, heat island, social vulnerability maps.
- **Tech:** ArcGIS.
- **Pricing:** Free, open data.
- **Similarity:** Directly usable Boston data source for flood/heat layers.

**UI/UX Analysis:**
- ArcGIS standard layout: sidebar for layers, full-screen map
- Blue for flooding, red/orange for heat data
- Predefined scenarios (9"/21"/36" sea level rise) instead of continuous slider
- Toggle layers to overlay climate risk + demographics for equity analysis
- **Strengths:** Comprehensive data. Overlay climate + social vulnerability is powerful.
- **Weaknesses:** Requires GIS literacy. Standard ArcGIS UI, not custom designed.

---

## AI + Map Guidance (Academic)

| Project | Description | Status |
|---------|-------------|--------|
| RouteLLM | Multi-agent LLM framework: natural language → constraint-aware routes | Research paper |
| MapGPT (ACL 2024) | LLM + topological maps for spatial reasoning | Academic PoC |
| LLMAP | LLM-as-Parser for multi-objective route planning with POIs | Research paper |

Note: Research shows LLMs are still unreliable as standalone path planners.

---

## Open-Source Building Blocks

| Library | Use for LightMap |
|---------|-----------------|
| `mapbox-gl-shadow-simulator` | Frontend shadow rendering (ShadeMap's engine) |
| `suncalc` (mourner) | JS sun/moon position calculation |
| `shadow-mapper` | Python shadow generation from OSM data |

---

## Industry-Standard UI/UX Patterns

### Layout
- **Full-screen map is universal.** Controls float over the map, never share equal space.
- **Time controls at bottom** — horizontal axis maps intuitively to time progression.
- **Layer controls in collapsible right panel** — accessible but out of the way.

### Color Conventions
| Data Type | Color | Used by |
|-----------|-------|---------|
| Shadow/shade | Grey / dark | ShadeMap |
| Water / flooding | Blue | Climate Ready Boston, First Street |
| Heat / high risk | Red / orange | Climate Ready Boston, First Street |
| Brightness / lit areas | Yellow → white | Safest Way, Light Pollution Map |
| Safety / low risk | Green | First Street |
| Intensity heatmaps | Dark → blue → green → red | ShadeMap, Light Pollution Map |

### Interaction
- **Click-to-inspect is expected.** Users expect to click any point and get data. Products that lack this are criticized.
- **Overlay opacity control** — critical for any data overlay on a base map (Light Pollution Map proves this at 60% default).
- **Two base maps minimum** — road/cartographic + satellite.
- **Search-by-location** — address or coordinate search is essential.

### What to Avoid
- Inverted/unconventional time sliders (ShadeMap criticism)
- Non-collapsible controls that eat screen space (Shadowmap criticism)
- No map legend (First Street criticism)
- Unable to click map features for info (First Street criticism)
- Scientific units without plain-language translation (Light Pollution Map barrier)
- No onboarding — every product lacks this and it hurts casual users

---

## LightMap Boston Differentiation

**No existing product combines daytime shade + nighttime brightness + weather hazards on one map.**

| Feature | ShadeMap | Safest Way | First Street | Climate Ready Boston | LightMap Boston |
|---------|----------|------------|--------------|---------------------|-----------------|
| Daytime shadow | Yes | - | - | - | Yes |
| Nighttime brightness | - | Yes | - | - | Yes |
| Weather hazards | - | - | Yes (flood) | Yes (flood + heat) | Yes |
| AI guidance | - | - | - | - | Yes (planned) |
| Boston-specific | - | - | Partial | Yes | Yes |
| Visualization (not routing) | Yes | No (routes) | Yes | Yes | Yes |
