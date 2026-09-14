---
id: brso.exposure.ead
layer: ontology
kind: concept
title: Exposure at Default (EAD)
version: brso-v0.1
status: ACTIVE
concept_type: BusinessConcept
domain: exposure
description: A governed exposure measure representing the amount expected to be outstanding
  or otherwise exposed at the time of default under the applicable methodology.
parent_id: brso.exposure.exposure_measure
relationships:
- type: IS_A
  target: brso.exposure.exposure_measure
  approval_status: approved
  confidence: 1.0
- type: MEASURED_BY
  target: brso.foundation.currency
  approval_status: approved
  confidence: 1.0
- type: AS_OF
  target: brso.foundation.date
  approval_status: approved
  confidence: 1.0
---
# Exposure at Default (EAD)

A governed exposure measure representing the amount expected to be outstanding or otherwise exposed at the time of default under the applicable methodology.
