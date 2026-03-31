# P4 — Selection as Class Project Direction

## Purpose

This document evaluates P4 (Urban Environment Public Health Mapping) against the narrowing criteria from the map-based exploration document and records the decision to adopt it as the class project direction.

## Evaluation Against Criteria

| Criterion | Verdict | Notes |
|---|---|---|
| One-semester feasible | ✅ | Four foundational layers (shade, lighting, weather hazard, canopy) each buildable on public data. Web deployment achievable with a modest stack (FastAPI + MapLibre GL JS). |
| Anchored in Boston + Cambridge | ✅ | The spatial scope is the course's spatial scope by construction. Boston and Cambridge open-data portals provide the municipal inputs directly. |
| Public data only | ✅ | OpenStreetMap, municipal open data, NOAA / Open-Meteo, public incident data. No IRB, no DUA, no gated access. |
| Preventive angle | ✅ | Each layer is a property of the environment *before* an adverse event, not a response after. |
| Intuitive for non-specialist audience | ✅ | A map is among the few presentation substrates that work without training. Residents read their neighborhood directly. |

All five criteria satisfied. The other four candidate concepts from the exploration document fail at least one (C1 reactive, C2/C3 saturated by existing work, C4 saturated by mature local work, or all requiring marginal contribution rather than a coherent project).

## Continuity with Prior Exploration

The earlier synthesis across P1, P2, and P3 extracted five architectural commitments: integration of heterogeneous data, support for human decisions, deployability, safety-with-personalization, and scale. P4 realizes each of these on a different substrate — urban environmental data instead of clinical data, residents instead of clinicians, a public web application instead of a hospital deployment — while preserving the same underlying architectural posture. Adopting P4 does not discard the prior exploration; it extends the same discipline into an implementation layer that is accessible, preventive, and visually intuitive.

## Decision

P4 is adopted as the class project direction for 1.001.

## Next Steps

The immediate next concrete steps, in order:

1. **Initial urban mapping project plan.** Draft a scoped project plan covering which municipal datasets are fetched, how they are transformed, and what the initial deployable surface looks like.
2. **Narrow the layer mix toward shade and brightness.** Of the four foundational layers, shade-by-day and brightness-by-night are the two most decision-relevant for everyday resident use and the two that have the tightest feasibility profile in a single semester. Prioritize them first; weather hazards and canopy are additions.
3. **Choose a working project name.** A name that reflects the shade-by-day / light-by-night framing cleanly; this will make the rest of the work easier to describe internally and externally.
4. **Build a first deployable prototype.** FastAPI backend, MapLibre frontend, OpenStreetMap buildings for Boston, initial shade engine. Iterate from there.

These next steps are the subject of the documents and commits that follow in the project history.
