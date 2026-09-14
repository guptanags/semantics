from pathlib import Path
import re
import yaml

class OkfParser:
    """Parses the project's OKF Markdown convention, including multi-document files."""

    _DOC_RE = re.compile(r"^---\s*$", re.MULTILINE)

    def parse_many(self, path: str | Path) -> list[dict]:
        text = Path(path).read_text(encoding="utf-8")
        markers = list(self._DOC_RE.finditer(text))
        if not markers:
            raise ValueError(f"Missing YAML frontmatter: {path}")
        documents = []
        for i in range(0, len(markers), 2):
            if i + 1 >= len(markers):
                raise ValueError(f"Unclosed YAML frontmatter: {path}")
            fm_text = text[markers[i].end():markers[i+1].start()]
            body_start = markers[i+1].end()
            body_end = markers[i+2].start() if i + 2 < len(markers) else len(text)
            frontmatter = yaml.safe_load(fm_text) or {}
            body = text[body_start:body_end].strip()
            if "id" not in frontmatter:
                raise ValueError(f"Missing id: {path}")
            documents.append({"frontmatter": frontmatter, "body": body, "path": str(path)})
        return documents

    def parse(self, path: str | Path) -> dict:
        docs = self.parse_many(path)
        if len(docs) != 1:
            raise ValueError(f"Expected one OKF document in {path}; found {len(docs)}")
        return docs[0]
