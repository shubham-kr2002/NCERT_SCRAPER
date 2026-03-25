from __future__ import annotations

import re

from ncert_scraper.models import DiscoveryRecord


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "_", value.strip())
    return cleaned.strip("_") or "Unknown"


def stable_id(class_name: str, subject: str, book: str, chapter: str, language: str) -> str:
    key = f"{class_name}|{subject}|{book}|{chapter}|{language}"
    return slugify(key).lower()


def chapter_filename(record: DiscoveryRecord) -> str:
    return f"{slugify(record.class_name)}_{slugify(record.subject)}_{slugify(record.chapter)}.pdf"

