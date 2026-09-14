class PathResolver:
    """Deterministic metadata path selection.

    Ranking:
      1. certified
      2. preferred
      3. cardinality safety
      4. fewer joins
    """

    def choose(self, candidates: list[dict]) -> dict:
        if not candidates:
            raise ValueError("No valid metadata join path")
        return sorted(
            candidates,
            key=lambda x: (
                not x.get("certified", False),
                not x.get("preferred", False),
                x.get("cardinality") != "MANY_TO_ONE",
                x.get("join_count", 999),
            ),
        )[0]
