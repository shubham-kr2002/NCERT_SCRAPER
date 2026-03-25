from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from ncert_scraper.models import CrawlState
from ncert_scraper.utils.io import read_json, write_json


class StateStore:
    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self, seeds: Iterable[str]) -> CrawlState:
        raw = read_json(self.path, default=None)
        if raw is None:
            return CrawlState(queue=list(seeds), visited=[])
        return CrawlState.model_validate(raw)

    def save(self, state: CrawlState) -> None:
        payload = state.model_dump(mode="json")
        payload["last_checkpoint"] = datetime.now(timezone.utc).isoformat()
        write_json(self.path, payload)

