# Synthesis Across Three Healthcare AI Prototypes

## Purpose

This document steps back from P1, P2, and P3 individually and looks at what they share. The goal is not to rank them or pick a winner — each is a legitimate direction with substantive ideas — but to notice what architectural principles keep reappearing across three otherwise quite different prototype designs.

## Summary of the Three Prototypes

| | P1 | P2 | P3 |
|---|----|----|----|
| **Working title** | Population-Scale Drug Response Analytics | Individualized Longitudinal Risk Modeling AI | Research-to-Practice Bridge Framework for Clinical AI |
| **Primary input** | Observational clinical cohorts (EHR, claims, registries via OMOP) | Multi-modal patient data (genotype, biomarkers, imaging, clinical phenotype) | FHIR-standardized clinical data + any upstream model |
| **Primary method** | Causal ML for subgroup treatment effects | Longitudinal sequence models (transformer / GNN / HMM) | Reference architecture + lifecycle loop + monitoring |
| **Primary audience** | Pharmacoepidemiologist / public-health analyst | Clinician / patient-facing care workflow | Clinical informatics / MLOps / deployment team |
| **Core output** | Subgroup-conditional treatment effect with uncertainty | Per-patient risk trajectory over time | Operational substrate for any clinical AI in production |

Three different problems, three different audiences. On the surface they look like unrelated design exercises.

## MedCombo

[MedCombo](https://github.com/JuhongPark/medcombo) was started during the same topic-selection phase as a related medication-combination analysis project and was later developed further as a separate project.
It explored reviewing combinations of medicines for possible drug-drug interaction concerns, duplicated ingredients, overlapping therapeutic classes, and cases where pharmacist or clinician review would be appropriate.

## Recurring Architectural Commitments

Pulling the three apart surfaces five architectural commitments that show up in each, in different shape:

### 1. Integration of heterogeneous data

| P1 | EHR + claims + trial registries, harmonized via OMOP CDM |
| P2 | Genotype + biomarkers + imaging + clinical phenotype, aligned longitudinally |
| P3 | FHIR resources (Patient, Observation, Condition, Medication, Encounter) pulled from disparate EHRs |

Every prototype begins by merging data from multiple modalities or sources into something usable. The specific substrates differ; the commitment does not.

### 2. Support for decisions made by humans

| P1 | Surface subgroup-level treatment effects with uncertainty to an analyst |
| P2 | Present trajectories, modifiable factors, and next-evaluation timing to a clinician / patient |
| P3 | Wrap any model in a deployment substrate that surfaces to bedside workflow |

None of these prototypes proposes to replace a human decision-maker. All three are AI-as-assistant architectures.

### 3. Deployability and real-world integration

| P1 | Federated architecture to meet data where it lives (Sentinel, OHDSI) |
| P2 | Multi-cohort validation, especially ancestry-balanced; careful governance |
| P3 | Explicit lifecycle loop with prospective monitoring; the whole prototype is deployability |

Every prototype has to confront the gap between controlled evaluation and operational environment. P3 is named for this; P1 and P2 both treat it as a first-order concern.

### 4. Safety and personalization

| P1 | Subgroup-conditional output implies personalized matching of therapy to patient context |
| P2 | Longitudinal trajectory with individualized contributing factors |
| P3 | XAI and monitoring as safety primitives baked in at the framework level |

Safety and personalization ride together. Each prototype wants to surface *who* is at risk and *why*, not just whether a risk exists on average.

### 5. Scale beyond a single clinic or a single patient

| P1 | Population-cohort scale by construction |
| P2 | Bio-bank scale (UK Biobank, ADNI) for training; per-patient at inference |
| P3 | Hospital-system scale as the target deployment context |

The ambition is always larger than a single institution or a single patient visit.

## Observation

Three prototypes from three different technical corners of healthcare AI land, independently, on the same five architectural commitments. This is not accidental — it reflects what a serious healthcare AI design in the current landscape *requires*. Data integration, decision support, deployability, safety-with-personalization, and scale: these are the building blocks, regardless of which specific healthcare problem one starts from.

## Open Question

The five commitments are stated in the language of the three prototypes: clinical cohorts, hospitals, patients. But the commitments themselves are abstract — integration, decision support, deployment, safety, scale — and nothing about them is intrinsically bound to a bedside or a pharmacy.

**Can the same commitments be realized in a different implementation layer — a different *substrate* for the data, a different *audience* for the decision, a different *context* for the deployment — while preserving the architectural discipline these prototypes share?**

This question is deliberately left open. It sets the stage for subsequent conversations with faculty advisors on where to take the work next.
