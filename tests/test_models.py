import pytest
from pydantic import ValidationError

from ncert_scraper.models import DiscoveryRecord, Language


def test_discovery_record_validates_url_fields() -> None:
    with pytest.raises(ValidationError):
        DiscoveryRecord(
            stable_id="x",
            class_name="10",
            subject="Science",
            book="Science",
            chapter="Chapter 1",
            source_page="not-a-url",
            download_url="https://ncert.nic.in/jesc101.pdf",
        )


def test_discovery_record_language_enum() -> None:
    record = DiscoveryRecord(
        stable_id="x",
        class_name="10",
        subject="Science",
        book="Science",
        chapter="Chapter 1",
        language=Language.ENGLISH,
        source_page="https://ncert.nic.in/textbook.php?jesc=10-1",
        download_url="https://ncert.nic.in/jesc101.pdf",
    )
    assert record.language == Language.ENGLISH

