import zipfile
from pathlib import Path

from ncert_scraper.processing.rag_processor import RagProcessor


def test_extract_zip_and_list_files(tmp_path: Path) -> None:
    zip_path = tmp_path / "book.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("a.txt", "hello")
        zf.writestr("b\\c.txt", "world")

    out = tmp_path / "out"
    files = RagProcessor().extract_zip(zip_path, out)
    assert any(p.name == "a.txt" for p in files)
    assert any(p.name == "c.txt" for p in files)


def test_inject_metadata_for_pdf(tmp_path: Path) -> None:
    pdf = tmp_path / "x.pdf"
    pdf.write_bytes(b"%PDF-1.4")
    metadata_path = RagProcessor().inject_metadata_for_pdf(pdf, {"class": "10"})
    assert metadata_path.exists()
    assert '"class": "10"' in metadata_path.read_text(encoding="utf-8")

