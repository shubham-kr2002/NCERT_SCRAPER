from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ncert_scraper.models import DiscoveryRecord


@dataclass(frozen=True)
class DiscoveryFilter:
    class_name: Optional[str] = None
    subject: Optional[str] = None
    language: Optional[str] = None

    def allows(self, record: DiscoveryRecord) -> bool:
        if self.class_name and record.class_name.lower() != self.class_name.lower():
            return False
        if self.subject and record.subject.lower() != self.subject.lower():
            return False
        if self.language and record.language.value.lower() != self.language.lower():
            return False
        return True

