from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


class Language(str, Enum):
    ENGLISH = "English"
    HINDI = "Hindi"
    URDU = "Urdu"
    UNKNOWN = "Unknown"


class CrawlError(BaseModel):
    url: str
    stage: str
    message: str
    retryable: bool = False
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CrawlMeta(BaseModel):
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    finished_at: Optional[datetime] = None
    pages_visited: int = 0
    links_found: int = 0
    valid_assets: int = 0
    duplicates_removed: int = 0
    failures: int = 0
    schema_version: str = "1.0.0"


class DiscoveryRecord(BaseModel):
    stable_id: str
    class_name: str
    subject: str
    book: str
    chapter: str
    language: Language = Language.UNKNOWN
    book_id: Optional[str] = None
    source_page: HttpUrl
    download_url: HttpUrl
    breadcrumbs: list[str] = Field(default_factory=list)


class DiscoveryManifest(BaseModel):
    meta: CrawlMeta
    records: list[DiscoveryRecord]
    errors: list[CrawlError] = Field(default_factory=list)


class CrawlState(BaseModel):
    queue: list[str] = Field(default_factory=list)
    visited: list[str] = Field(default_factory=list)
    last_checkpoint: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

