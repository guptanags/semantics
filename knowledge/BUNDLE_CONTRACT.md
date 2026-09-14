# OKF bundle contract — v0.1

## Layering

```text
Ontology bundle
  Business concepts + approved business relationships

Semantic bundle
  Semantic Data Element + Logical Dataset

Metadata bundle
  Physical Data Asset + Physical Column + certified Join Path
```

## Cross-layer references

| From | Relationship | To | Meaning |
|---|---|---|---|
| Concept | REPRESENTED_BY | SemanticDataElement | The governed data element represents the business concept |
| SemanticDataElement | ELEMENT_PART_OF_DATASET | LogicalDataset | Element belongs to a logical analytical dataset |
| LogicalDataset | IMPLEMENTED_BY | PhysicalDataAsset | Logical dataset is implemented by a physical table/view |
| SemanticDataElement | ELEMENT_IMPLEMENTED_BY_COLUMN | PhysicalColumn | Direct physical implementation of the semantic element |
| PhysicalDataAsset | ASSET_HAS_COLUMN | PhysicalColumn | Column membership |
| PhysicalDataAsset | ASSET_JOINS_TO_ASSET | PhysicalDataAsset | Certified physical join path |

## Why both semantic and metadata mappings exist

A semantic element expresses business meaning and analytical behavior. A physical column expresses storage. The direct implementation edge allows deterministic SQL planning without collapsing business semantics into physical metadata.

## Example resolution chain

```text
"party EAD"
 -> brso.exposure.ead
 -> brso.semantic.party_ead
 -> brso.dataset.party_exposure
 -> brso.asset.fact_exposure
 -> brso.column.fact_exposure.ead
 -> SUM(FACT_EXPOSURE.EAD)
```

## Metadata join safety

Join paths carry:
- cardinality
- preferred flag
- certified flag
- join type
- exact source and target columns

The query planner must prefer certified paths and reject ambiguous or unsafe join graphs rather than selecting an arbitrary shortest path.
