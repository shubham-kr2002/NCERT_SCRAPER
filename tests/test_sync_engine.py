import asyncio
from pathlib import Path

import pytest

from ncert_scraper.models import DiscoveryRecord, Language
from ncert_scraper.sync.downloader import SyncEngine


class DummyResponse:
    def __init__(self, headers=None, content=b"x", status_ok=True):
        self.headers = headers or {"content-length": "1"}
        self.content = content
        self._status_ok = status_ok

    def raise_for_status(self) -> None:
        if not self._status_ok:
            raise RuntimeError("status error")


class DummyClient:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return None

    async def head(self, url: str, follow_redirects: bool = True):
        return DummyResponse(headers={"content-length": "4"})

    async def get(self, url: str, follow_redirects: bool = True):
        return DummyResponse(content=b"data")


class EmptyHeadClient(DummyClient):
    async def head(self, url: str, follow_redirects: bool = True):
        return DummyResponse(headers={"content-length": "0"})


def _record() -> DiscoveryRecord:
    return DiscoveryRecord(
        stable_id="x",
        class_name="10",
        subject="Science",
        book="Textbook",
        chapter="Chapter 1",
        language=Language.ENGLISH,
        source_page="https://ncert.nic.in/textbook.php?jesc=10-1",
        download_url="https://ncert.nic.in/jesc101.pdf",
    )


def _settings(tmp_path: Path):
    class TestSettings:
        OUTPUT_ROOT = tmp_path / "NCERT_Data"
        USER_AGENT = "test"

    return TestSettings


def test_sync_engine_downloads_and_writes_metadata(tmp_path: Path, monkeypatch) -> None:
    import ncert_scraper.sync.downloader as mod

    monkeypatch.setattr(mod.httpx, "AsyncClient", lambda **kwargs: DummyClient())
    engine = SyncEngine(settings=_settings(tmp_path), max_concurrency=1)
    results = asyncio.run(engine.run([_record()], delay_ms=0))
    assert len(results) == 1
    target = tmp_path / "NCERT_Data" / "10" / "Science" / "Textbook" / "Chapters" / "10_Science_Chapter_1.pdf"
    assert target.exists()
    assert target.with_suffix(".metadata.json").exists()


def test_sync_engine_raises_on_empty_head(tmp_path: Path, monkeypatch) -> None:
    import ncert_scraper.sync.downloader as mod

    monkeypatch.setattr(mod.httpx, "AsyncClient", lambda **kwargs: EmptyHeadClient())
    engine = SyncEngine(settings=_settings(tmp_path), max_concurrency=1)
    with pytest.raises(ValueError):
        asyncio.run(engine.run([_record()], delay_ms=0))

