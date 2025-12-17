from datetime import datetime, timezone
from typing import List

import feedparser  # type: ignore

from mini_agent import Tech
from mini_agent.sources import get_sources
from mini_agent.state.sub_state import RawEvent
from mini_agent.types import SourceType


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
            out.append(
                RawEvent(
                    source=self.key,
                    fetched_at=fetched_at,
                    payload={
                        "url": url,
                        "feed": getattr(d, "feed", {}),
                        "entries": getattr(d, "entries", []),
                    },
                )
            )
        return out
