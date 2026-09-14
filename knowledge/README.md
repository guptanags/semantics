# Knowledge bundles

The project uses three governed OKF layers:

- `ontology/` — BRSO business concepts and approved business relationships.
- `semantic/` — governed semantic data elements and logical datasets.
- `metadata/` — physical data assets, columns and certified join paths.

The layers are deliberately separated. A business concept must never directly reference a physical table or column. The bridge is:

```text
BRSO Concept
  -> REPRESENTED_BY
Semantic Data Element
  -> ELEMENT_PART_OF_DATASET
Logical Dataset
  -> IMPLEMENTED_BY
Physical Data Asset
  -> ASSET_HAS_COLUMN
Physical Column
```

A semantic element may additionally connect to the physical column that implements it through `ELEMENT_IMPLEMENTED_BY_COLUMN`.
