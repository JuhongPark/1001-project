# Map-Based Healthcare System Concepts — Exploration

## Purpose

Following the direction shift recorded in the previous document, this survey takes the question seriously: *what does a map-based, intuitively legible healthcare system actually look like?* The goal is to collect candidate concepts, check which are feasible within a one-semester project, and narrow toward something concrete.

## Precedent: The Cholera Map as Baseline

The archetypal map-based public-health tool is now more than 170 years old. In 1854 John Snow mapped cholera deaths in Soho, London, around the Broad Street water pump; the spatial clustering around a single pump is visible at a glance and implicates a contaminated water source without any statistical training on the reader's part [1]. The map did three things that later work still tries to do:

- It joined location data to health outcome data on a single visual surface.
- It surfaced a pattern intelligible to a non-specialist audience.
- It suggested an intervention (remove the pump handle) that did not require further interpretation.

Snow's map is the canonical case for the proposition that place-based visualization can make complex population-health signals broadly legible. Modern GIS in epidemiology inherits this posture, applied to contemporary data.

## Candidate Concepts

Five candidates were surveyed for whether a map-based implementation could meaningfully serve a non-specialist audience on a one-semester timeline with public data.

### C1 — Disease-spread maps

Real-time or near-real-time mapping of contagious disease incidence at a neighborhood or census-tract level. COVID-era dashboards normalized this category; many public health departments now maintain ongoing disease-surveillance maps. Public data (CDC, state DPH) is available.

### C2 — Healthcare access maps (hospitals, specialty services)

Maps of travel time, cost, and availability to primary care, emergency departments, specialty care, or pharmacies. USDA and HHS maintain access atlases at the national level. Recent geospatial analyses have linked ACS data to access metrics at national, state, and county granularity [2].

### C3 — Mental health service access maps

A subset of C2, specifically for mental health providers. Current research documents barriers including limited provider supply, financial barriers, and lack of linguistically and culturally appropriate care [3]. A visualization could surface supply deserts at the neighborhood level.

### C4 — Food access / food desert maps

The USDA Food Access Research Atlas provides a canonical map-based tool at the national level [4]. Boston-specific work includes the Metropolitan Area Planning Council's Massachusetts Food Systems Map and the Boston Abundance App, which surface affordable food options in real time [5][6]. This is a mature category with multiple operational examples.

### C5 — Urban environment health-determinant maps

Mapping the built environment itself — shade, tree canopy, lighting at night, walkability, heat-island exposure, flood and ice hazards — as a population-health signal. A map of the *physical conditions* under which residents navigate their city, interpreted as a continuous population-health input rather than a single snapshot of disease.

This category is less standardized than C2 / C4 but benefits from a large inventory of open public datasets: OpenStreetMap for buildings and roads, city GIS departments for streetlight and canopy data, NOAA / Open-Meteo for weather, and municipal open-data portals for incident and infrastructure data.

## Narrowing Criteria

Four criteria were applied:

- **One-semester feasibility.** Can a scoped prototype be produced by a small team in a semester using only public data?
- **Anchor in Boston / Cambridge.** Does the concept admit a concrete local instance, to satisfy the course's spatial scope and to test the work against a real place?
- **Public data only.** No gated clinical cohorts, no proprietary EHR access, no institutional DUAs.
- **Preventive angle.** Does the map surface a signal that supports *decisions before* an adverse event, not only after?

| Candidate | Semester feasible | Boston anchor | Public data | Preventive |
|---|---|---|---|---|
| C1 Disease spread | Partial (data lag) | Yes | Yes | Reactive mainly |
| C2 Healthcare access | Yes | Yes | Yes | Partial |
| C3 Mental health access | Yes (smaller scope) | Yes | Partial | Partial |
| C4 Food deserts | Yes | Yes (mature work) | Yes | Partial |
| C5 Urban environment health determinants | Yes | Yes | Yes | Yes |

## Observations

A few patterns emerged during the survey:

- **C1 (disease spread)** is valuable but fundamentally reactive; the relevant signal exists after cases occur. It is closer to surveillance than prevention.
- **C2 and C3 (healthcare and mental-health access)** are well served by existing federal and state tools. Another neighborhood-level map would add marginal value unless it introduced a novel data source.
- **C4 (food access)** is a mature category with Boston-specific operational instances already in use. Entering this category would mean contributing at the margin of active, local work.
- **C5 (urban environment health determinants)** is less saturated, naturally preventive, and has a deep inventory of public data waiting to be combined. The built environment is an underused population-health input.

## Convergence

Of the five candidates, **C5 — urban environment health determinants** is the strongest fit across all four narrowing criteria. It is semester-feasible with public data, it is natively anchored in a specific city, and it is structurally preventive rather than reactive.

It is also the candidate in which the five architectural commitments from the synthesis — data integration, decision support, deployability, safety-with-personalization, and scale — map most directly onto a non-clinical substrate. Each commitment has a clean analogue in the urban-environment context:

- Integration: merging buildings, streetlights, weather, canopy, and hazard data on one surface.
- Decision support: helping residents make everyday spatial decisions — where to walk, when to be outside.
- Deployability: a public web application is a real deployment target, not a hypothetical hospital integration.
- Safety and personalization: routes and exposures vary by person and time of day.
- Scale: a city (Boston + Cambridge) rather than a single clinic.

## Transition

The next document defines this concept (C5) in the same depth applied to P1–P3, as a fourth and converged prototype direction.

## References

1. "Revisiting John Snow's Cholera Map: A Data Visualisation Case Study for Statistical Education," *arXiv*, 2025.
2. "Geospatial Analysis of Access to Health Care and Internet Services in the US," *PMC*, 2022.
3. Boston CHNA-CHIP Collaborative Community Health Needs Assessment, 2022.
4. USDA Economic Research Service, "Food Access Research Atlas."
5. Metropolitan Area Planning Council (MAPC), "Massachusetts Food Access Index Model."
6. Boston Medical Center HealthCity, "Should We Still Be Saying 'Food Desert'?"
