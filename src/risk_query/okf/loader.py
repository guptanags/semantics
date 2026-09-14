from pathlib import Path
from risk_query.okf.parser import OkfParser
from risk_query.okf.validator import OkfValidator
from risk_query.okf.relationship_extractor import RelationshipExtractor

class OkfLoader:
    """Loads a complete OKF layer and validates all references before mutation."""

    def load(self, directory: str):
        parser = OkfParser()
        validator = OkfValidator()
        extractor = RelationshipExtractor()
        documents, relationships = [], []
        for path in sorted(Path(directory).glob("*.okf.md")):
            for doc in parser.parse_many(path):
                validator.validate(doc)
                documents.append(doc)
                relationships.extend(extractor.extract(doc))
        ids = {d["frontmatter"]["id"] for d in documents}
        missing = sorted({r["target_id"] for r in relationships if r["target_id"] not in ids})
        if missing:
            raise ValueError(f"Unresolved OKF relationship targets: {missing}")
        return documents, relationships
