# Semantic Data Graph Bundle

Each OKF document describes a governed semantic element or logical dataset.

Required semantic element fields:
- `id`
- `layer: semantic`
- `kind: semantic_data_element`
- `concept_id`
- `logical_dataset_id`
- `physical_column_id` when directly implemented by a column
- `semantic_type`
- `grain`
- `version`
- `status`

Metrics additionally declare aggregation semantics, e.g. EAD -> `SUM`.
