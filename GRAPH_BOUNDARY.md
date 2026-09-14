# Graph Boundary Architecture

The system uses **three disjoint Kùzu graph stores**. They are not one federated Kùzu graph.

```text
┌──────────────────────┐
│     ONTOLOGY GRAPH   │
│                      │
│ Concept              │
│ RelationshipType     │
│ RelationshipAssertion│
│ SemanticRole         │
└──────────────────────┘
          ║
          ║ external IDs only
          ║
┌──────────────────────┐
│    SEMANTIC GRAPH    │
│                      │
│ SemanticDataElement  │
│ LogicalDataset       │
└──────────────────────┘
          ║
          ║ external IDs only
          ║
┌──────────────────────┐
│    METADATA GRAPH    │
│                      │
│ PhysicalDataAsset    │
│ PhysicalColumn       │
│ Join relationships   │
└──────────────────────┘

        +-------------------------+
        | Federation Registry     |
        | (outside all graphs)    |
        |                         |
        | concept -> semantic     |
        | dataset -> asset        |
        | element -> column       |
        +-------------------------+
