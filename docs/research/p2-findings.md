# Prototype P2 — Findings

## What Was Sketched

The P2 exploration produced a four-layer design for longitudinal, multi-modal risk trajectory modeling:

- A Mermaid diagram for the input → aligner → longitudinal encoder → trajectory head → clinical view pipeline
- A catalog of modality-specific input pipelines (genotype, biomarkers, imaging, clinical phenotype)
- An architecture shortlist for the longitudinal encoder (transformers, temporal GNNs, personalized HMMs)
- A list of cohort substrates with their respective access profiles (ADNI, UK Biobank, dbGaP-gated genomic sources)

As with P1, no implementation was produced; the purpose was to test whether this direction is a viable prototype path.

## Key Technical Findings

**1. The modeling stack is mature and documented.** AI-optimized polygenic risk scoring combined with proteomics and imaging has demonstrated meaningful AUC lifts on public benchmarks. Personalized HMMs and transformer-style sequence models have both been applied to longitudinal neurodegenerative cohorts with published results. The design can borrow heavily from prior work rather than invent.

**2. Data access is multi-headed and slow.** Unlike P1, where one harmonized schema (OMOP) covers most of the data question, P2 pulls from several cohorts, each with its own application, review timeline, and governance. Genetic arms gated through dbGaP add their own layer. Even for a scoped prototype the paperwork budget is substantial.

**3. The discipline of bias control is non-negotiable.** Polygenic reference panels remain skewed toward European ancestry, and uncritical application to diverse populations reproduces rather than resolves inequity. Multi-ancestry validation is a first-class design element, not a final-stage audit.

**4. The interpretive leap is the hard part.** The pipeline can produce a calibrated trajectory per patient. Turning that into something a clinician integrates into care — modifiable vs. non-modifiable contributors, decision-relevant thresholds, communication to patients — is the part where prior work most consistently stalls.

## Feasibility Judgment (Concept-Level, R10)

If pursued as a real project, P2 would need:

- Multi-cohort data-access applications in parallel, with timelines measured in months per cohort
- A larger collaborator network than P1: genetics / clinical neurology / imaging / biostatistics
- GPU compute for sequence-model training over multi-modal inputs; durable storage for imaging data
- An ethics / equity review track running alongside the technical work, not after it

At class-project scale, a scoped demonstration on a pre-cleared ADNI slice is plausible; an end-to-end multi-cohort instance is out of reach in one semester.

## Open Questions for Further Exploration

- What is the right user interface for presenting a *trajectory* — a time-valued object — to a decision-maker who is used to point estimates?
- How should modifiable contributors (environmental, behavioral) be visually separated from non-modifiable ones (age, specific variants)?
- At what point in a care pathway should longitudinal risk trajectories actually enter the workflow?
- Are there population-level substrates — not genetic but environmental or spatial — on which similar trajectory-modeling ideas could reach broader audiences with lower access barriers?
