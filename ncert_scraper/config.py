from __future__ import annotations

from pathlib import Path
from typing import Sequence


class Settings:
    BASE_URL = "https://ncert.nic.in"
    START_URLS: Sequence[str] = (
        "https://ncert.nic.in/textbook.php",
        "https://ncert.nic.in/ebooks.php",
    )
    OUTPUT_ROOT = Path("NCERT_Data")
    ARTIFACT_ROOT = Path(".ncert_artifacts")
    CATALOG_JSON = ARTIFACT_ROOT / "catalog.json"
    CATALOG_JSONL = ARTIFACT_ROOT / "catalog.jsonl"
    ERRORS_JSON = ARTIFACT_ROOT / "errors.json"
    CRAWL_STATE_JSON = ARTIFACT_ROOT / "crawl_state.json"
    USER_AGENT = "ncert-scraper/0.1.0 (+discovery-agent)"

