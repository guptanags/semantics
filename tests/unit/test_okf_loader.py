from risk_query.okf.parser import OkfParser

def test_parser_reads_frontmatter(tmp_path):
    p = tmp_path / "x.okf.md"
    p.write_text("""---
id: brso.party.corporate
title: Corporate
version: brso-v0.1
status: ACTIVE
---
# Corporate
A corporate party.
""")
    doc = OkfParser().parse(p)
    assert doc["frontmatter"]["id"] == "brso.party.corporate"
