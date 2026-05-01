# MIT 1.001 Term Project

A graduate-level term project for MIT 1.001: Engineering Computation and Data Science, taught by Abel Sanchez and John R. Williams.

## Background

Several directions were considered for the 1.001 term project.
Healthcare AI systems, an area of interest, became the direction pursued further.
[MedCombo](https://github.com/JuhongPark/medcombo), a related medication-combination analysis project, was started during this phase as part of the 1.001 healthcare AI exploration and was later developed further as a separate project.
It explored whether software could help review combinations of medicines by surfacing possible drug interaction concerns, duplicated ingredients, overlapping therapeutic classes, and cases where pharmacist or clinician review would be appropriate.
During that exploration, faculty feedback suggested pursuing a more intuitive direction; the search then continued within healthcare for something that could be realized through map-based visualization.

## Final Project Direction

The direction selected was an AI system that maps urban environment and public health. The result is LightMap — a real-time map of shade during the day and lighting at night in Boston and Cambridge, Massachusetts, computed from sun position, building geometry, streetlights, tree canopy, and weather. It approaches healthcare AI systems from a preventive public-health angle: shade maps to heat stress and UV exposure, nighttime lighting to pedestrian safety, weather hazards to falls and injuries.

## Project history

### Setup (March 21)
- Mar 21 — Repository created; course project documentation added; workspace gitignores configured.

### Healthcare AI systems exploration (March 22 – 31)
- Mar 22 — Landscape survey of healthcare AI systems.
- Mar 23 – 28 — Candidate directions within healthcare AI systems explored. See `docs/research/`.
- Mar 23 – 28 — [MedCombo](https://github.com/JuhongPark/medcombo) started alongside the healthcare AI topic-selection work as a medication-combination analysis project and was later developed further.
- Mar 29 — Synthesis across the exploration.
- Mar 30 — Faculty review session. Feedback toward a more intuitive direction.
- Mar 30 – 31 — Map-based healthcare concepts surveyed. Urban environment × public health mapping selected.

### LightMap implementation (April 1 onward)
- Apr 1 — Initial plan → scope set to Boston and Cambridge, Massachusetts → rewritten as a "shade by day, light by night" map → project named LightMap.
- Apr 1 — Data catalog, shadow engine, prototype maps. FastAPI + MapLibre GL JS web app. Weather and hazard overlays, 46K buildings, tree canopy layer, UI polish.
- Apr 4 — Competitive analysis (Shadowmap.org), plan overhaul, Phase 5 submission readiness.
- Apr 5 — Rain / snow feature feasibility, data source verification.

## Repository layout

- `docs/research/` — landscape survey, candidate-direction notes, synthesis, faculty feedback, map-based concept survey
- `docs/plan.md` — project plan
- `docs/prototyping-plan.md` — prototyping plan
- `docs/competitive-research.md` — competitive analysis
- `docs/data-catalog.md` — data sources
- `docs/prototype-day.html`, `docs/prototype-night.html` — early prototype maps
- `src/` — shadow engine and FastAPI backend

## Continuation

Development of LightMap continues in a [separate repository](https://github.com/JuhongPark/lightmap).
