class QuerySecurityPolicy:
    def __init__(self, allowed_objects: set[str] | None = None, max_rows: int = 10000):
        self.allowed_objects = allowed_objects or set()
        self.max_rows = max_rows

    def authorize(self, sql: str):
        return True
