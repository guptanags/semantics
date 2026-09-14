class QueryExecutor:
    def __init__(self, connection=None, security=None, dry_run=True):
        self.connection = connection
        self.security = security
        self.dry_run = dry_run

    def execute(self, sql: str):
        if self.security:
            self.security.authorize(sql)

        if self.dry_run:
            return []

        if self.connection is None:
            raise RuntimeError("No analytical database connection configured")
        return self.connection.execute(sql)
