# Database Metadata Graph Bundle

This bundle represents physical database metadata only.

Kinds:
- `physical_data_asset` — table/view/materialized object.
- `physical_column` — governed physical column.
- `physical_join` — certified or preferred join path with cardinality.

A physical join is metadata, not business meaning. Its purpose is deterministic query planning and validation.
