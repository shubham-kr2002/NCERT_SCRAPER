from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urljoin, urlparse

from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from ncert_scraper.config import Settings


def _same_host(base_url: str, target_url: str) -> bool:
    return urlparse(base_url).netloc == urlparse(target_url).netloc


@dataclass(frozen=True)
class ExtractedLink:
    href: str
    text: str
    source_url: str
    breadcrumbs: list[str]


class BrowserSession:
    def __init__(self, user_agent: str = Settings.USER_AGENT) -> None:
        self.user_agent = user_agent

    def __enter__(self) -> tuple[Browser, BrowserContext]:
        self._playwright = sync_playwright().start()
        browser = self._playwright.chromium.launch(headless=True)
        context = browser.new_context(user_agent=self.user_agent)
        return browser, context

    def __exit__(self, exc_type, exc, tb) -> None:
        self._playwright.stop()


class RouteExplorer:
    def __init__(self, base_url: str = Settings.BASE_URL, delay_ms: int = 250) -> None:
        self.base_url = base_url
        self.delay_ms = delay_ms

    def discover_links(self, page: Page, current_url: str) -> list[ExtractedLink]:
        anchors = page.locator("a[href]").all()
        links: list[ExtractedLink] = []
        for anchor in anchors:
            href = anchor.get_attribute("href")
            text = anchor.inner_text(timeout=1000).strip()
            if not href:
                continue
            absolute = urljoin(current_url, href)
            if not _same_host(self.base_url, absolute):
                continue
            breadcrumbs = [item.strip() for item in text.split(">") if item.strip()]
            links.append(ExtractedLink(href=absolute, text=text, source_url=current_url, breadcrumbs=breadcrumbs))
        return links

    def visit(self, page: Page, url: str) -> None:
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(self.delay_ms)

