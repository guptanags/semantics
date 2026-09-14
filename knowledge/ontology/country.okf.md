---
id: brso.geography.country
layer: ontology
kind: concept
title: Country
version: brso-v0.1
status: ACTIVE
concept_type: BusinessConcept
domain: geography
description: A governed geographic or jurisdictional concept representing a country
  used in party, regulatory, booking, market, or risk classification.
parent_id: brso.geography.geography
relationships:
- type: IS_A
  target: brso.geography.geography
  approval_status: approved
  confidence: 1.0
- type: PART_OF_GEOGRAPHY
  target: brso.geography.region
  approval_status: approved
  confidence: 1.0
---
# Country

A governed geographic or jurisdictional concept representing a country used in party, regulatory, booking, market, or risk classification.
