---
id: brso.exposure.exposure
layer: ontology
kind: concept
title: Exposure
version: brso-v0.1
status: ACTIVE
concept_type: BusinessConcept
domain: exposure
description: A governed representation of the bank's economic or risk-relevant amount
  at stake with respect to a party, facility, transaction, market factor, country,
  industry, or other risk-bearing object.
parent_id: brso.foundation.measurement
relationships:
- type: AGAINST
  target: brso.foundation.party
  approval_status: approved
  confidence: 1.0
- type: MEASURED_BY
  target: brso.foundation.measurement
  approval_status: approved
  confidence: 1.0
- type: AS_OF
  target: brso.foundation.date
  approval_status: approved
  confidence: 1.0
---
# Exposure

A governed representation of the bank's economic or risk-relevant amount at stake with respect to a party, facility, transaction, market factor, country, industry, or other risk-bearing object.
