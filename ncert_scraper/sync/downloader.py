from __future__ import annotations

import asyncio
from pathlib import Path

import httpx

from ncert_scraper.config import Settings
from ncert_scraper.discovery.manifest import ManifestBuilder
from ncert_scraper.models import DiscoveryRecord
from ncert_scraper.utils.io import write_json
from ncert_scraper.utils.naming import chapter_filename, slugify


class SyncEngine:
    def __init__(self, settings: type[Settings] = Settings, max_concurrency: int = 5) -> None:
        self.settings = settings
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def _download_record(self, client: httpx.AsyncClient, record: DiscoveryRecord) -> dict:
        async with self.semaphore:
            head = await client.head(str(record.download_url), follow_redirects=True)
            head.raise_for_status()
            if int(head.headers.get("content-length", "1")) <= 0:
                raise ValueError(f"empty content for {record.download_url}")

            chapter_dir = (
                self.settings.OUTPUT_ROOT
                / slugify(record.class_name)
                / slugify(record.subject)
                / slugify(record.book)
                / "Chapters"
            )
            chapter_dir.mkdir(parents=True, exist_ok=True)
            file_path = chapter_dir / chapter_filename(record)

            response = await client.get(str(record.download_url), follow_redirects=True)
            response.raise_for_status()
            file_path.write_bytes(response.content)

            metadata = {
                "class": record.class_name,
                "subject": record.subject,
                "book": record.book,
                "chapter_name": record.chapter,
                "language": record.language.value,
                "source_url": str(record.source_page),
                "download_url": str(record.download_url),
                "book_id": record.book_id,
            }
            write_json(file_path.with_suffix(".metadata.json"), metadata)
            return {"stable_id": record.stable_id, "path": str(file_path), "bytes": len(response.content)}

    async def run(self, records: list[DiscoveryRecord], delay_ms: int = 200) -> list[dict]:
        if not records:
            return []
        timeout = httpx.Timeout(45.0, connect=20.0)
        headers = {"User-Agent": self.settings.USER_AGENT}
        async with httpx.AsyncClient(timeout=timeout, headers=headers) as client:
            tasks = []
            for record in records:
                tasks.append(self._download_record(client, record))
                await asyncio.sleep(delay_ms / 1000.0)
            return await asyncio.gather(*tasks)

    @staticmethod
    def load_records(path: Path = Settings.CATALOG_JSON) -> list[DiscoveryRecord]:
        return ManifestBuilder.load_records(path)

