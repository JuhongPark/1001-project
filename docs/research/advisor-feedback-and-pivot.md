# Advisor Feedback and Direction Shift

## Meeting Context

As part of the 1.001 class project review, the three prototype directions — P1 (Population-Scale Drug Response Analytics), P2 (Individualized Longitudinal Risk Modeling AI), and P3 (Research-to-Practice Bridge Framework for Clinical AI) — were presented to the course faculty, Prof. Abel Sanchez and Prof. John R. Williams, in a project review session.

The purpose of the session was to step back after the initial exploration phase and decide where to focus development effort for the remainder of the semester.

## What Was Presented

For each prototype: the problem statement, the design-level architecture sketch (the Mermaid diagrams from the concept docs), the key technical findings, and the feasibility considerations captured in the findings docs. The synthesis across all three prototypes, including the five shared architectural commitments, was presented alongside.

The question opened to the faculty was essentially: *which of these is the right direction to develop further, and how should the class project be scoped around it?*

## Faculty Response

The response from the faculty on the three directions themselves was positive. Each prototype was acknowledged as a substantive exploration of a real problem; no direction was criticized or dismissed.

The substantive input came in the form of a direction for *further* development rather than a judgment on the prior work. Paraphrased:

> When you develop this further, aim for something more intuitive. Let the end state be something a person can look at and immediately understand, not something that requires expert interpretation.

This was offered in the spirit of orienting the *next step* — choosing a vehicle for the ideas already explored — rather than as a retrospective grade on what had been built.

## Interpretation

"Intuitive" here is doing real work. Reading the three prototypes through the lens of that suggestion, a consistent observation emerges: each of P1, P2, and P3 produces output that a *specialist* can act on — a pharmacoepidemiologist, a clinician, a deployment engineer. The work assumed an expert audience because each domain, on its own, does. The faculty's prompt pushes the other way: toward something a non-specialist can meaningfully engage with.

The fastest path from "specialist-legible" to "broadly-legible" is visualization. Specifically, *spatial* visualization — a map — is unusual in that it reads correctly for audiences with no technical training. Almost anyone can look at a map, see where something is concentrated, and form an opinion. Few other presentation substrates share this property.

## Connection to the Synthesis

The synthesis across P1–P3 identified five recurring architectural commitments: integration of heterogeneous data, support for human decisions, deployability, safety and personalization, and scale. Each of those was observed in the language of its original domain — patient data, clinical workflow, hospital infrastructure — but each is itself abstract.

The open question at the end of the synthesis asked whether those same commitments could be realized in a different *implementation layer*: a different substrate for the data, a different audience for the decisions, a different context for deployment.

The faculty's input to make it *intuitive* converges neatly with that question. The implementation layer that makes healthcare AI broadly legible — and makes the underlying commitments reach a non-specialist — is one built around *intuitive spatial visualization*. A map-based layer.

## Direction Shift

Concretely, the direction shifts from three domain-specialized prototype studies to one integrated exploration: **healthcare AI implemented through map-based spatial visualization, aimed at a non-specialist audience, operating at a population rather than clinical scale.**

The shift is not a reversal. The five commitments from the synthesis are kept. The methodological rigor explored in P1 (data integration with robustness), P2 (multi-modal longitudinal modeling), and P3 (deployability with monitoring) are kept. What changes is the substrate and the audience: from patient records and clinicians, to place-based data and people navigating a real environment.

## Next Step

Survey map-based healthcare system concepts — what has been tried, where public data can support a one-semester project, what kinds of decisions a map-based tool can meaningfully support for a broad audience. This is the subject of the next document.
