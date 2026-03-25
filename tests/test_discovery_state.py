from pathlib import Path

from ncert_scraper.discovery.state import StateStore
from ncert_scraper.models import CrawlState


def test_state_store_loads_seed_when_missing(tmp_path: Path) -> None:
    store = StateStore(tmp_path / "crawl_state.json")
    state = store.load(["https://ncert.nic.in/textbook.php"])
    assert state.queue == ["https://ncert.nic.in/textbook.php"]
    assert state.visited == []


def test_state_store_save_and_reload(tmp_path: Path) -> None:
    path = tmp_path / "crawl_state.json"
    store = StateStore(path)
    original = CrawlState(queue=["a", "b"], visited=["x"])
    store.save(original)
    loaded = store.load([])
    assert loaded.queue == ["a", "b"]
    assert loaded.visited == ["x"]

