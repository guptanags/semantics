from pathlib import Path
import re


SRC = Path(__file__).parents[2] / "src" / "risk_query"


def test_no_comma_separated_match_patterns():
    """Kùzu compatibility guard: keep independent MATCH clauses separate."""
    offenders = []
    pattern = re.compile(r"MATCH\s+[^\n]*\),\s*\(")
    for path in SRC.rglob("*.py"):
        text = path.read_text()
        for line_no, line in enumerate(text.splitlines(), 1):
            if pattern.search(line):
                offenders.append(f"{path}:{line_no}:{line.strip()}")
    assert offenders == [], "Kùzu-incompatible comma-separated MATCH found:\n" + "\n".join(offenders)


def test_no_reserved_keyword_column_parameters():
    """Kùzu compatibility guard: $column is a reserved keyword in Kùzu Cypher parser."""
    offenders = []
    pattern = re.compile(r"\$column\b")
    for path in SRC.rglob("*.py"):
        text = path.read_text()
        for line_no, line in enumerate(text.splitlines(), 1):
            if pattern.search(line):
                offenders.append(f"{path}:{line_no}:{line.strip()}")
    assert offenders == [], "Kùzu-incompatible reserved parameter $column found:\n" + "\n".join(offenders)

