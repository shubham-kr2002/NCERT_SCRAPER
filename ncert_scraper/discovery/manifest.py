from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from ncert_scraper.models import CrawlError, CrawlMeta, DiscoveryManifest, DiscoveryRecord
from ncert_scraper.utils.io import append_jsonl, read_json, write_json


class ManifestBuilder:
    def __init__(self, catalog_json: Path, catalog_jsonl: Path, errors_json: Path) -> None:
        self.catalog_json = catalog_json
        self.catalog_jsonl = catalog_jsonl
        self.errors_json = errors_json
        self.meta = CrawlMeta()
        self.records_by_id: dict[str, DiscoveryRecord] = {}
        self.errors: list[CrawlError] = []

    def add_record(self, record: DiscoveryRecord) -> None:
        self.meta.links_found += 1
        if record.stable_id in self.records_by_id:
            self.meta.duplicates_removed += 1
            return
        self.records_by_id[record.stable_id] = record
        self.meta.valid_assets += 1
        append_jsonl(self.catalog_jsonl, record.model_dump(mode="json"))

    def add_error(self, error: CrawlError) -> None:
        self.meta.failures += 1
        self.errors.append(error)

    def set_pages_visited(self, count: int) -> None:
        self.meta.pages_visited = count

    def save(self) -> DiscoveryManifest:
        self.meta.finished_at = datetime.now(timezone.utc)
        manifest = DiscoveryManifest(meta=self.meta, records=list(self.records_by_id.values()), errors=self.errors)
        write_json(self.catalog_json, manifest.model_dump(mode="json"))
        write_json(self.errors_json, [e.model_dump(mode="json") for e in self.errors])
        return manifest

    @staticmethod
    def load_records(path: Path) -> list[DiscoveryRecord]:
        raw = read_json(path, default={"records": []})
        return [DiscoveryRecord.model_validate(item) for item in raw.get("records", [])]

