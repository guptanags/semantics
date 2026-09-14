from pathlib import Path

class OkfValidator:
    REQUIRED = {"id", "title", "version", "status"}

    def validate(self, document: dict):
        fm = document["frontmatter"]
        missing = self.REQUIRED - fm.keys()
        if missing:
            raise ValueError(f"Missing OKF fields: {sorted(missing)}")
        if not str(fm["id"]).startswith("brso."):
            raise ValueError(f"Non-BRSO identifier: {fm['id']}")
        return True

    def validate_directory(self, directory: str):
        parser = __import__("risk_query.okf.parser", fromlist=["OkfParser"]).OkfParser()
        for path in Path(directory).glob("*.okf.md"):
            self.validate(parser.parse(path))
