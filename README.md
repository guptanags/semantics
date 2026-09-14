## Federated graph boundary

The runtime now uses three physically disjoint Kùzu databases:

- `data/kuzu/ontology` — business ontology only.
- `data/kuzu/semantic` — governed semantic data elements and logical datasets.
- `data/kuzu/metadata` — physical assets, columns and joins.

There are intentionally **no cross-graph Kùzu relationships**. Stable IDs such as `concept_id` in the semantic graph are external references, not ontology graph edges. Semantic-to-physical bindings are maintained in `config/federation.yaml`, an application-level federation registry outside all three graphs. This preserves the rule that the ontology is not aware of the data model.

## Kùzu compatibility

This release removes comma-separated multi-pattern `MATCH` clauses from the ingestion path and uses separate `MATCH` clauses, which is compatible with the Kùzu parser encountered during local ingestion. A regression test prevents reintroduction of this pattern.

Validation performed in the build environment:
- Python source compilation: PASS
- Unit/integration tests: 8 passed
- Static audit of all Python/Cypher query sources for comma-separated `MATCH`: PASS

**Note:** the build environment used to produce this archive does not have the Kùzu Python package/native runtime installed, so a live Kùzu database ingestion could not be executed here. The release is therefore not represented as live-Kùzu-tested in this environment.

# Risk Semantic Query

A Python reference implementation of the Semantic Data Resolution / Access Layer for Corporate & Investment Banking (CIB) and Risk.

## Architecture

```text
Scenario / Business Query
        |
        v
+-----------------------+
| Query Intent           |
| LLM normalization      |  <-- Vertex AI
+-----------+-----------+
            |
            v
+-----------------------+
| Ontology Resolver      |
| Semantic Resolver      |
| Entity/Metric Resolver |
+-----------+-----------+
            |
            v
+-----------------------+
| Metadata / Path        |
| Resolution             |
+-----------+-----------+
            |
            v
+-----------------------+
| Deterministic Query    |
| Planner                |
+-----------+-----------+
            |
            v
+-----------------------+
| Deterministic SQL      |
| Generator + Validator  |
+-----------+-----------+
            |
            v
       Database
```

Reverse direction:

```text
SQL -> SQL AST -> Metadata -> Semantic Data -> Ontology -> Business Explanation
```

## Key design rules

1. Vertex AI extracts and normalizes intent; it does not generate executable SQL.
2. Query resolution is deterministic after intent extraction.
3. Ambiguous concepts are surfaced rather than guessed.
4. Grain, join cardinality, temporal validity and aggregation semantics are first-class.
5. A semantic graph cannot invent unavailable facts.
6. Scenario impact scoring remains outside this component.
7. Ontology, semantic data and physical metadata are separate graph layers.
8. OKF is the interchange/persistence bundle format; the BRSO model is the banking-specific semantic contract.
9. Production traversal should use only approved relationship assertions.
10. Every result should carry provenance and resolution status.

## Run

```bash
pip install -e .

python -m risk_query.graph.schema --db ./data/kuzu/brso
risk-query
```

The implementation is intentionally a reference architecture. Production deployments should add enterprise IAM, secrets management, database adapters, query-cost controls, audit persistence, RLS integration and stronger ontology governance.

## OKF graph ingestion

The repository now contains sample Semantic Data Graph and Database Metadata Graph bundles.

```bash
python -m risk_query.okf.cli \
  --db ./data/kuzu/brso \
  --ontology ./knowledge/ontology \
  --semantic ./knowledge/semantic \
  --metadata ./knowledge/metadata
```

The ingestion sequence is:

```text
OKF parse
  -> layer validation
  -> cross-layer reference validation
  -> ontology graph
  -> metadata graph
  -> semantic graph
  -> semantic-to-physical bridge
```

The pipeline validates references before writes. For production, replace the small ontology fixture with the governed BRSO ontology bundle and add atomic staging/promotion around the complete graph load.
