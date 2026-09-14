---
id: brso.geography.geography
layer: ontology
kind: concept
title: Geography
version: brso-v0.1
status: ACTIVE
concept_type: BusinessConcept
domain: geography
description: A canonical geographic area used to describe location, jurisdiction,
  market presence, risk, booking, or revenue attribution.
parent_id: brso.foundation.concept
relationships:
- type: PART_OF_GEOGRAPHY
  target: brso.geography.geography
  approval_status: approved
  confidence: 1.0
- type: CONTAINS_GEOGRAPHY
  target: brso.geography.geography
  approval_status: approved
  confidence: 1.0
---
# Geography

A canonical geographic area used to describe location, jurisdiction, market presence, risk, booking, or revenue attribution.
