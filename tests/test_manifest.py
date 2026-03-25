from pathlib import Path

from ncert_scraper.discovery.manifest import ManifestBuilder
from ncert_scraper.discovery.normalizer import normalize_record


def test_manifest_deduplicates(tmp_path: Path) -> None:
    builder = ManifestBuilder(
        catalog_json=tmp_path / "catalog.json",
        catalog_jsonl=tmp_path / "catalog.jsonl",
        errors_json=tmp_path / "errors.json",
    )
    record = normalize_record(
        source_page="https://ncert.nic.in/textbook.php?jesc=10-1",
        download_url="https://ncert.nic.in/jesc101.pdf",
        class_name="10",
        subject="Science",
        book="Science",
        chapter="Chapter1",
        breadcrumbs=["Science"],
    )
    builder.add_record(record)
    builder.add_record(record)
    manifest = builder.save()
    assert len(manifest.records) == 1
    assert manifest.meta.duplicates_removed == 1

