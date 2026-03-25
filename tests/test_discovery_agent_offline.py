from pathlib import Path

import ncert_scraper.discovery.agent as agent_mod
from ncert_scraper.discovery.agent import DiscoveryAgent, DiscoveryOptions
from ncert_scraper.discovery.navigator import ExtractedLink


class FakePage:
    pass


class FakeContext:
    def new_page(self) -> FakePage:
        return FakePage()


class FakeBrowserSession:
    def __enter__(self):
        return (None, FakeContext())

    def __exit__(self, exc_type, exc, tb):
        return None


class FakeRouteExplorer:
    def __init__(self, delay_ms: int = 0) -> None:
        self.delay_ms = delay_ms

    def visit(self, page: FakePage, url: str) -> None:
        return None

    def discover_links(self, page: FakePage, current_url: str):
        return [
            ExtractedLink(
                href="https://ncert.nic.in/jesc101.pdf",
                text="Chapter 1",
                source_url=current_url,
                breadcrumbs=["Science"],
            ),
            ExtractedLink(
                href="https://ncert.nic.in/next",
                text="Next",
                source_url=current_url,
                breadcrumbs=["Science"],
            ),
        ]


def _settings(tmp_path: Path):
    class TestSettings:
        START_URLS = ("https://ncert.nic.in/start",)
        CRAWL_STATE_JSON = tmp_path / "crawl_state.json"
        CATALOG_JSON = tmp_path / "catalog.json"
        CATALOG_JSONL = tmp_path / "catalog.jsonl"
        ERRORS_JSON = tmp_path / "errors.json"
        USER_AGENT = "test"

    return TestSettings


def test_discovery_agent_offline_generates_records(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(agent_mod, "BrowserSession", FakeBrowserSession)
    monkeypatch.setattr(agent_mod, "RouteExplorer", FakeRouteExplorer)
    agent = DiscoveryAgent(settings=_settings(tmp_path))
    manifest = agent.run(DiscoveryOptions(class_name="10", subject="Science", max_pages=1, dry_run=False))
    assert len(manifest.records) == 1
    assert manifest.records[0].subject == "Science"
    assert (tmp_path / "catalog.json").exists()


def test_discovery_agent_dry_run_skips_snapshot_write(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(agent_mod, "BrowserSession", FakeBrowserSession)
    monkeypatch.setattr(agent_mod, "RouteExplorer", FakeRouteExplorer)
    agent = DiscoveryAgent(settings=_settings(tmp_path))
    manifest = agent.run(DiscoveryOptions(class_name="10", subject="Science", max_pages=1, dry_run=True))
    assert len(manifest.records) == 0
    assert not (tmp_path / "catalog.json").exists()
    assert (tmp_path / "crawl_state.json").exists()

