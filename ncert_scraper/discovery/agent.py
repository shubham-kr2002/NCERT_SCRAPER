from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Optional

from playwright.sync_api import Error as PlaywrightError

from ncert_scraper.config import Settings
from ncert_scraper.discovery.filtering import DiscoveryFilter
from ncert_scraper.discovery.manifest import ManifestBuilder
from ncert_scraper.discovery.navigator import BrowserSession, RouteExplorer
from ncert_scraper.discovery.normalizer import normalize_record
from ncert_scraper.discovery.state import StateStore
from ncert_scraper.models import CrawlError, CrawlState, DiscoveryManifest


@dataclass(frozen=True)
class DiscoveryOptions:
    class_name: Optional[str] = None
    subject: Optional[str] = None
    language: Optional[str] = None
    max_pages: int = 120
    resume: bool = True
    dry_run: bool = False
    delay_ms: int = 250


class DiscoveryAgent:
    def __init__(self, settings: type[Settings] = Settings) -> None:
        self.settings = settings
        self.state_store = StateStore(settings.CRAWL_STATE_JSON)
        self.manifest = ManifestBuilder(settings.CATALOG_JSON, settings.CATALOG_JSONL, settings.ERRORS_JSON)

    def run(self, options: DiscoveryOptions) -> DiscoveryManifest:
        filters = DiscoveryFilter(options.class_name, options.subject, options.language)
        state = self.state_store.load(self.settings.START_URLS) if options.resume else CrawlState(queue=list(self.settings.START_URLS), visited=[])
        queue = deque(state.queue or list(self.settings.START_URLS))
        visited = set(state.visited)
        explorer = RouteExplorer(delay_ms=options.delay_ms)

        with BrowserSession() as (_, context):
            page = context.new_page()
            while queue and len(visited) < options.max_pages:
                url = queue.popleft()
                if url in visited:
                    continue
                visited.add(url)
                try:
                    explorer.visit(page, url)
                    for link in explorer.discover_links(page, url):
                        if link.href not in visited and link.href not in queue:
                            queue.append(link.href)
                        if not (link.href.endswith(".zip") or link.href.endswith(".pdf")):
                            continue
                        record = normalize_record(
                            source_page=link.source_url,
                            download_url=link.href,
                            class_name=options.class_name or "UnknownClass",
                            subject=options.subject or "UnknownSubject",
                            book=link.breadcrumbs[0] if link.breadcrumbs else "UnknownBook",
                            chapter=link.text or "UnknownChapter",
                            breadcrumbs=link.breadcrumbs,
                        )
                        if filters.allows(record):
                            self.manifest.add_record(record)
                except PlaywrightError as exc:
                    self.manifest.add_error(
                        CrawlError(url=url, stage="navigate", message=str(exc), retryable=True)
                    )
                state.queue = list(queue)
                state.visited = list(visited)
                self.state_store.save(state)
        self.manifest.set_pages_visited(len(visited))
        if options.dry_run:
            return DiscoveryManifest(meta=self.manifest.meta, records=[], errors=self.manifest.errors)
        return self.manifest.save()

