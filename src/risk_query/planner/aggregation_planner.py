class AggregationPlanner:
    def validate(self, measure_aggregation: str, grain: str | None):
        if measure_aggregation == "SUM" and not grain:
            return ["Measure has SUM but no declared semantic grain."]
        return []
