class SqlGenerator:
    """Deterministic SQL builder.

    The planner supplies physical objects in production. This class never asks
    the LLM to write SQL.
    """

    def generate(self, plan):
        if not plan.root_dataset_id:
            raise ValueError("No physical root dataset resolved")

        raise NotImplementedError(
            "Populate physical dataset/column bindings from the metadata graph "
            "before SQL generation."
        )
