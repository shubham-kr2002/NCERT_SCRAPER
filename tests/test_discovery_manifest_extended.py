from pathlib import Path

from ncert_scraper.discovery.manifest import ManifestBuilder
from ncert_scraper.discovery.normalizer import normalize_record
from ncert_scraper.models import CrawlError


def _record() -> object:
    return normalize_record(
        source_page="https://ncert.nic.in/textbook.php?jesc=10-1",
        download_url="https://ncert.nic.in/jesc101.pdf",
        class_name="10",
        subject="Science",
        book="Science",
        chapter="Chapter1",
        breadcrumbs=["Science"],
    )


def test_manifest_writes_errors_and_metrics(tmp_path: Path) -> None:
    builder = ManifestBuilder(tmp_path / "catalog.json", tmp_path / "catalog.jsonl", tmp_path / "errors.json")
    builder.add_record(_record())
    builder.set_pages_visited(3)
    builder.add_error(CrawlError(url="https://ncert.nic.in/x", stage="navigate", message="boom", retryable=True))
    manifest = builder.save()
    assert manifest.meta.pages_visited == 3
    assert manifest.meta.failures == 1
    assert (tmp_path / "errors.json").exists()
    assert (tmp_path / "catalog.json").exists()
    assert (tmp_path / "catalog.jsonl").exists()

