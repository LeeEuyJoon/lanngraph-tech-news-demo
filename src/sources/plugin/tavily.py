import os
from datetime import datetime, timezone
from typing import List

from tavily import TavilyClient  # type: ignore

from src import Tech
from src.domain import SourceType
from src.state.sub_state import RawEvent


class TavilySource:
    """Tavily 웹 검색 소스 플러그인 (SearchSourcePlugin 구현)"""

    key = SourceType.TAVILY

    def search(self, *, tech: Tech, today: str, query: str) -> List[RawEvent]:
        """
        Tavily API로 웹 검색을 수행합니다.

        Args:
            tech: 기술 스택
            today: 오늘 날짜 (ISO 형식)
            query: 검색 쿼리 (필수)

        Returns:
            RawEvent 리스트
        """
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise ValueError("TAVILY_API_KEY environment variable is not set")

        client = TavilyClient(api_key=api_key)

        # Tavily 검색 실행
        results = client.search(
            query=query,
            max_results=5,
            search_depth="basic",
            include_answer=False,
            include_raw_content=False,
            days=15,
        )

        fetched_at = datetime.now(timezone.utc).isoformat()

        simplified_results = [
            {
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "content": result.get("content", ""),
                "published_date": result.get("published_date", ""),
            }
            for result in results.get("results", [])
        ]

        return [
            RawEvent(
                source=self.key,
                fetched_at=fetched_at,
                payload={
                    "query": query,
                    "results": simplified_results,
                },
            )
        ]
