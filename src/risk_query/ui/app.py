from pathlib import Path
from fastapi.responses import FileResponse

UI_DIR = Path(__file__).parent / "static"


def index():
    return FileResponse(UI_DIR / "index.html")
