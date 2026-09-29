"""Central configuration (overridable through environment variables)."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = os.environ.get("STUDYSPRINT_DB", str(BASE_DIR / "data" / "studysprint.db"))
LOG_DIR = Path(os.environ.get("STUDYSPRINT_LOG_DIR", BASE_DIR / "logs"))
LOG_FILE = LOG_DIR / "studysprint.log"

DEFAULT_EASE = 2.5
MIN_EASE = 1.3
MAX_NAME_LEN = 60
MAX_SESSION_MINUTES = 720  # 12 hours
