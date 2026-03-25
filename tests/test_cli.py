from pathlib import Path

from click.testing import CliRunner

import ncert_scraper.cli as cli_mod
from ncert_scraper.cli import cli
from ncert_scraper.models import CrawlMeta, DiscoveryManifest


class FakeDiscoveryAgent:
    def run(self, options):
        return DiscoveryManifest(meta=CrawlMeta(pages_visited=2, valid_assets=1, duplicates_removed=0, failures=0), records=[])


class FakeSyncEngine:
    def load_records(self):
        return ["x"]

    async def run(self, records, delay_ms: int = 0):
        return [{"stable_id": "x"}]


class FakeRagProcessor:
    def extract_zip(self, zip_path: Path, output_dir: Path):
        output_dir.mkdir(parents=True, exist_ok=True)
        return [output_dir / "a.txt"]


def test_cli_discover(monkeypatch) -> None:
    monkeypatch.setattr(cli_mod, "DiscoveryAgent", lambda: FakeDiscoveryAgent())
    result = CliRunner().invoke(cli, ["discover", "--class", "10", "--subject", "Science", "--dry-run"])
    assert result.exit_code == 0
    assert "discovery complete" in result.output


def test_cli_sync(monkeypatch) -> None:
    monkeypatch.setattr(cli_mod, "SyncEngine", lambda: FakeSyncEngine())
    result = CliRunner().invoke(cli, ["sync", "--delay-ms", "0"])
    assert result.exit_code == 0
    assert "sync complete: downloaded=1" in result.output


def test_cli_process_zip(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(cli_mod, "RagProcessor", lambda: FakeRagProcessor())
    zip_path = tmp_path / "x.zip"
    zip_path.write_bytes(b"PK\x03\x04")
    out = tmp_path / "out"
    result = CliRunner().invoke(cli, ["process-zip", str(zip_path), str(out)])
    assert result.exit_code == 0
    assert "zip extracted: files=1" in result.output

