# UI

The project now exposes a browser-based UI at `/` and `/ui`.

## Capabilities

- Browse the Kùzu graph across Ontology, Semantic Data and Database Metadata layers.
- Filter the visible layer and bound graph size.
- Select nodes to inspect IDs, type, layer and properties.
- Submit natural-language business queries through `POST /v1/query`.
- Show query resolution status, generated SQL, warnings and returned rows.
- Uses the same governed pipeline as the Scenario Engine path: Vertex AI intent extraction followed by deterministic graph resolution, planning, SQL generation and validation.

## Endpoints

- `GET /` — UI
- `GET /ui` — UI alias
- `POST /v1/graph/snapshot` — graph data for visualization
- `POST /v1/query` — natural-language query execution
- `POST /v1/scenario/query` — existing Scenario Engine integration
- `POST /v1/query/explain` — existing reverse-query scaffold

## Run

```bash
pip install -e .
risk-query
```

Open `http://localhost:8080/`.

The current project defaults to dry-run execution, so the UI can validate the semantic/planning path without executing against an analytical database.
