from ncert_scraper.discovery.normalizer import extract_book_id, infer_language
from ncert_scraper.models import Language


def test_extract_book_id_from_query() -> None:
    assert extract_book_id("https://ncert.nic.in/textbook.php?jesc=10-1") == "jesc"


def test_infer_language() -> None:
    assert infer_language("https://x/hindi/book.pdf", "") == Language.HINDI

