from __future__ import annotations

from urllib.parse import parse_qs, urlparse

from ncert_scraper.models import DiscoveryRecord, Language
from ncert_scraper.utils.naming import stable_id


def infer_language(url: str, text: str) -> Language:
    lowered = f"{url} {text}".lower()
    if "hindi" in lowered:
        return Language.HINDI
    if "urdu" in lowered:
        return Language.URDU
    if "english" in lowered:
        return Language.ENGLISH
    return Language.UNKNOWN


def extract_book_id(url: str) -> str | None:
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    if not query:
        return None
    return next(iter(query.keys()))


def normalize_record(
    source_page: str,
    download_url: str,
    class_name: str,
    subject: str,
    book: str,
    chapter: str,
    breadcrumbs: list[str],
) -> DiscoveryRecord:
    language = infer_language(download_url, " ".join(breadcrumbs))
    record_id = stable_id(class_name, subject, book, chapter, language.value)
    return DiscoveryRecord(
        stable_id=record_id,
        class_name=class_name.strip() or "UnknownClass",
        subject=subject.strip() or "UnknownSubject",
        book=book.strip() or "UnknownBook",
        chapter=chapter.strip() or "UnknownChapter",
        language=language,
        book_id=extract_book_id(source_page),
        source_page=source_page,
        download_url=download_url,
        breadcrumbs=[x.strip() for x in breadcrumbs if x.strip()],
    )

