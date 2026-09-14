from risk_query.domain.query_plan import QueryPlan

class QueryPlanner:
    def __init__(self, concept_resolver, metric_resolver):
        self.concept_resolver = concept_resolver
        self.metric_resolver = metric_resolver

    def plan(self, intent) -> QueryPlan:
        subject = self.concept_resolver.resolve(intent.subject)

        filters = []
        for f in intent.filters:
            concept = self.concept_resolver.resolve(f.concept)
            filters.append({
                "concept": concept,
                "operator": f.operator,
                "value_ids": f.value.resolved_ids,
                "value_text": f.value.text,
            })

        measures = []
        for m in intent.measures:
            concept = self.concept_resolver.resolve(m.concept)
            elements = self.metric_resolver.resolve(concept.concept_id)
            element_id = None
            rows = elements.get_all() if hasattr(elements, "get_all") else []
            if rows:
                # Kùzu returns a struct/object depending on version; this is a
                # reference placeholder for the semantic-element identifier.
                element_id = None
            measures.append({
                "concept": concept,
                "aggregation": m.aggregation,
                "semantic_element_id": element_id,
            })

        return QueryPlan(
            subject=subject,
            filters=filters,
            measures=measures,
            resolution_status="RESOLVED",
        )
