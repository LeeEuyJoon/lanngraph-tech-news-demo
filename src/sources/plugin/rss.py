from datetime import datetime, timezone
from typing import List

import feedparser  # type: ignore

from src import Tech
from src.sources import get_sources
from src.state.sub_state import RawEvent
from src.domain import SourceType


class RssSource:
    key = SourceType.RSS

    def fetch(self, *, tech: Tech, today: str) -> List[RawEvent]:
        # tech_sources.py에서 RSS URL 가져오기
        sources = get_sources(tech)
        urls = sources.get(SourceType.RSS, [])

        if not urls:
            return []

        fetched_at = datetime.now(timezone.utc).isoformat()
        out: List[RawEvent] = []

        for url in urls:
            d = feedparser.parse(url)

            # 필요한 필드만 추출하여 payload 크기 최소화
            entries = getattr(d, "entries", [])
            simplified_entries = [
                {
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "published": entry.get("published", ""),
                    "summary": entry.get("summary", ""),
                    "content": entry.get("content", [{}])[0].get("value", "") if entry.get("content") else "",
                    "author": entry.get("author", ""),
                }
                for entry in entries
            ]

            out.append(
                RawEvent(
                    source=self.key,
                    fetched_at=fetched_at,
                    payload={
                        "url": url,
                        "entries": simplified_entries,
                    },
                )
            )
        return out
