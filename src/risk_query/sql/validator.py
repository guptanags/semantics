import re

class SqlValidationError(Exception):
    pass

class SqlValidator:
    FORBIDDEN = [
        r"\bDROP\b", r"\bDELETE\b", r"\bUPDATE\b", r"\bINSERT\b",
        r"\bALTER\b", r"\bTRUNCATE\b", r"\bCREATE\b",
    ]

    def validate(self, sql: str, authorized_objects: set[str] | None = None):
        upper = sql.upper()
        for pattern in self.FORBIDDEN:
            if re.search(pattern, upper):
                raise SqlValidationError(f"Forbidden SQL operation: {pattern}")

        if re.search(r"\bCROSS\s+JOIN\b", upper):
            raise SqlValidationError("CROSS JOIN is not permitted")

        if authorized_objects:
            # Production implementation should parse AST and inspect identifiers.
            tokens = set(re.findall(r"\b[A-Z_][A-Z0-9_]*\b", upper))
            allowed = {x.upper() for x in authorized_objects}
            suspicious = {
                t for t in tokens
                if t.startswith(("FACT_", "DIM_", "CLIENT_", "ACCOUNT_"))
                and t not in allowed
            }
            if suspicious:
                raise SqlValidationError(f"Unauthorized objects: {sorted(suspicious)}")
        return True
