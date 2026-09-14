---
id: brso.industry.industry
layer: ontology
kind: concept
title: Industry
version: brso-v0.1
status: ACTIVE
concept_type: BusinessConcept
domain: industry
description: A canonical classification concept representing an economic sector or
  business activity used for segmentation, exposure attribution, reporting, or risk
  analysis.
parent_id: brso.industry.industry_classification
relationships:
- type: IS_A
  target: brso.industry.industry_classification
  approval_status: approved
  confidence: 1.0
- type: PART_OF
  target: brso.industry.industry
  approval_status: approved
  confidence: 1.0
- type: HAS_MEMBER
  target: brso.foundation.party
  approval_status: approved
  confidence: 1.0
---
# Industry

A canonical classification concept representing an economic sector or business activity used for segmentation, exposure attribution, reporting, or risk analysis.
