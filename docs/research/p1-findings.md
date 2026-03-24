# Prototype P1 — Findings

## What Was Sketched

The P1 exploration produced a design-level pipeline for population-scale drug response analytics:

- A three-layer architecture (cohort construction → causal-ML estimation → interpretable summary)
- A Mermaid diagram capturing the data and compute flow
- A data-infrastructure inventory (OMOP CDM, All of Us, Sentinel, ATLAS) sufficient to reason about where the data would come from
- A methods shortlist (causal forest / X-learner / TMLE; validation via negative controls and PS diagnostics)

No implementation was produced. The goal of the sketch was to assess whether the direction is viable within the class-project frame.

## Key Technical Findings

Working through the design surfaced several substantive observations:

**1. The scientific pathway is tractable.** Causal machine learning applied to OMOP-formatted observational data is an active and well-instrumented research area. Pipelines for CATE estimation with robustness checks are published, reproducible, and backed by mature tooling (`econml`, `causalml`, `DoWhy`; the OHDSI ecosystem on the OMOP side). The conceptual distance from problem statement to running pipeline is short when the data are in hand.

**2. Data access is the dominant gatekeeper.** The signal that makes this prototype interesting lives in large observational cohorts. Those cohorts are gated — either by IRB and institutional data use agreements (for identified EHR data), or by portal-controlled access (All of Us), or by federated-query-only access (Sentinel, some OHDSI partners). For proof-of-concept, synthetic datasets such as Synthea are immediately usable, but the results do not transfer to real-world claims.

**3. Robustness is not optional.** Observational causal inference has failure modes that do not disappear as the model class gets fancier. Any credible instance of this pipeline spends substantial effort on negative-control audits, propensity-score diagnostics, and sensitivity analyses against unmeasured confounding. Skipping this step produces confidently wrong estimates rather than improved ones.

**4. The natural audience is a specialist.** The most concrete end-user for P1 output is a pharmacoepidemiologist, biostatistician, or public-health analyst who can interrogate the estimates and their diagnostics. The output is numerical and conditional; it rewards methodological fluency.

## Feasibility Judgment (Concept-Level, R10)

If pursued as a real project, P1 would need:

- Formal data-access groundwork (IRB, DUA, or equivalent) measured in months
- A small interdisciplinary team: a pharmacoepidemiology domain expert, a causal-inference specialist, a data engineer familiar with OMOP
- Compute appropriate for large cohort queries — federated-friendly when datasets cannot be centralized
- An ongoing robustness-checking discipline, not just a one-shot model

At the class-project scale, a scoped demonstration on synthetic or publicly available OMOP data is achievable; a real-cohort result is not.

## Open Questions for Further Exploration

- What is the minimum cohort size at which subgroup-level CATE estimates become actionable rather than speculative?
- How is uncertainty best communicated to an analyst who is not a causal-inference specialist?
- In which deployment posture — analyst dashboard, regulatory submission, public-health surveillance — does this type of system reach a real decision, and what does the surrounding workflow look like?
- Are there settings in which similar causal-ML methods, applied to different substrates (environmental exposure, place-based risk), could reach a broader audience than specialists?
