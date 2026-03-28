# Prototype P3 — Findings

## What Was Sketched

The P3 exploration produced a reference-framework design, not a model. Specifically:

- A five-layer architecture (infrastructure, FHIR-based data, algorithm lifecycle, application, governance) drawn from recent systematic work on hospital AI platforms
- A lifecycle loop (develop → validate → deploy → monitor → retrain / rollback) with an explicit prospective-to-retrospective gap monitor
- A lessons-learned inventory from one canonical deployment failure (the Epic Sepsis Model) mapped onto the framework's layers
- A concrete tooling shortlist (HAPI, SMART on FHIR, HealthLake on the data side; Evidently, Seldon, WhyLabs on the monitoring side; SHAP, LIME, counterfactual methods as XAI layer)

The artifact is architectural, not algorithmic.

## Key Technical Findings

**1. The interoperability substrate is more usable than it used to be.** FHIR has crossed a practical threshold — standardized resources let AI services consume and emit clinical data without writing per-site adapters. This reduces a whole category of engineering cost that used to dominate clinical AI deployment.

**2. The failure modes that matter are not model-quality failures.** They are data-leakage, population-shift, alert-fatigue, and silent-drift failures. The Epic Sepsis Model case study surfaces all of these. A framework that improves clinical AI has to address these modes directly and by construction, not as an afterthought.

**3. Monitoring is a first-class system, not a dashboard.** Post-deployment monitoring of prospective performance, with predefined rollback thresholds, has to exist before launch. Waiting for an academic paper to flag a problem takes years.

**4. The framework is a substrate, not a product.** P3 does not propose a specific clinical AI — it proposes the scaffolding that any such AI needs to be responsibly deployed into a hospital environment. Without a concrete clinical use case on top, the scaffolding is still useful but remains abstract.

## Feasibility Judgment (Concept-Level, R10)

If pursued as a real project, P3 would need:

- A partnered hospital environment with real FHIR endpoints and clinical leadership commitment
- A cross-functional team spanning clinical informatics, MLOps, UX, compliance, security
- A clinical use case sitting on top of the framework (likely borrowed from existing research, including but not limited to directions like P1 or P2)
- Sustained engagement over months-to-years, because the failure modes it addresses are operational and only manifest after launch

At class-project scope, a *reference* implementation is realistic: the architecture documented, a worked example on a toy model, and a post-mortem of a documented failure case reinterpreted through the framework's lens. A live hospital deployment is not within reach.

## Open Questions for Further Exploration

- What is the right level of abstraction — a generic framework that spans clinical domains, or specialized variants per domain?
- How should the framework behave in small-institution or resource-constrained settings where in-house FHIR expertise is scarce?
- Does the same deployment posture transfer outside the hospital — to community-level, public-health, or population-health systems that operate on non-clinical data but face the same trust and deployment questions?
- If we strip the framework of its clinical-specific assumptions, what remains? And where does that abstract remainder point?
