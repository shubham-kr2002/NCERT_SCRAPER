from ncert_scraper.discovery.normalizer import normalize_record
from ncert_scraper.utils.naming import chapter_filename, slugify, stable_id


def test_slugify_handles_symbols() -> None:
    assert slugify(" Class 10 / Science ") == "Class_10_Science"


def test_stable_id_is_lowercase_and_deterministic() -> None:
    sid = stable_id("10", "Science", "Textbook", "Chapter 1", "English")
    assert sid == "10_science_textbook_chapter_1_english"


def test_chapter_filename_format() -> None:
    record = normalize_record(
        source_page="https://ncert.nic.in/textbook.php?jesc=10-1",
        download_url="https://ncert.nic.in/jesc101.pdf",
        class_name="10",
        subject="Science",
        book="Science",
        chapter="Chapter 1",
        breadcrumbs=["Science"],
    )
    assert chapter_filename(record) == "10_Science_Chapter_1.pdf"

