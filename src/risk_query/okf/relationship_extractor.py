from typing import Any

class RelationshipExtractor:
    def extract(self, document: dict) -> list[dict[str, Any]]:
        fm = document["frontmatter"]
        result = []
        for rel in fm.get("relationships", []) or []:
            result.append({
                "relationship_type": rel["type"],
                "source_id": fm["id"],
                "target_id": rel["target"],
                "confidence": float(rel.get("confidence", 1.0)),
                "approval_status": rel.get("approval_status", "approved"),
                "valid_from": rel.get("valid_from"),
                "valid_to": rel.get("valid_to"),
                "source_reference": document["path"],
            })
        return result
