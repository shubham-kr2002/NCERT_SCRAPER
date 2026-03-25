from __future__ import annotations

import zipfile
from pathlib import Path

from ncert_scraper.utils.io import write_json


class RagProcessor:
    def extract_zip(self, zip_path: Path, output_dir: Path) -> list[Path]:
        output_dir.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(output_dir)
        return [path for path in output_dir.rglob("*") if path.is_file()]

    def inject_metadata_for_pdf(self, pdf_path: Path, metadata: dict) -> Path:
        metadata_path = pdf_path.with_suffix(".metadata.json")
        write_json(metadata_path, metadata)
        return metadata_path

