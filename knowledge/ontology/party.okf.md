---
id: brso.foundation.party
layer: ontology
kind: concept
title: Party
version: brso-v0.1
status: ACTIVE
concept_type: BusinessConcept
domain: foundation
description: A legally or operationally identifiable actor that can participate in
  financial, contractual, risk, ownership, or reporting relationships.
relationships:
- type: HAS_PRIMARY_INDUSTRY
  target: brso.industry.industry
  approval_status: approved
  confidence: 1.0
- type: OPERATES_IN
  target: brso.geography.geography
  approval_status: approved
  confidence: 1.0
- type: DOMICILED_IN
  target: brso.geography.country
  approval_status: approved
  confidence: 1.0
- type: HAS_EXPOSURE
  target: brso.exposure.exposure
  approval_status: approved
  confidence: 1.0
- type: HAS_FACILITY
  target: brso.corporate.credit_facility
  approval_status: approved
  confidence: 1.0
---
# Party

A legally or operationally identifiable actor that can participate in financial, contractual, risk, ownership, or reporting relationships.
