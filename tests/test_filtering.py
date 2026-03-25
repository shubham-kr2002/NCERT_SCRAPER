from ncert_scraper.discovery.filtering import DiscoveryFilter
from ncert_scraper.discovery.normalizer import normalize_record


def test_filter_allows_matching_record() -> None:
    record = normalize_record(
        source_page="https://ncert.nic.in/textbook.php?abc=10-1",
        download_url="https://ncert.nic.in/abc101.pdf",
        class_name="10",
        subject="Science",
        book="Science",
        chapter="Chapter 1",
        breadcrumbs=["Science"],
    )
    filt = DiscoveryFilter(class_name="10", subject="science")
    assert filt.allows(record)

