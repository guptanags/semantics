from pathlib import Path
import kuzu

class KuzuConnection:
    def __init__(self, database_path: str):
        Path(database_path).parent.mkdir(parents=True, exist_ok=True)
        self.db = kuzu.Database(database_path)
        self.conn = kuzu.Connection(self.db)

    def execute(self, query: str, parameters: dict | None = None):
        if parameters:
            return self.conn.execute(query, parameters)
        return self.conn.execute(query)
