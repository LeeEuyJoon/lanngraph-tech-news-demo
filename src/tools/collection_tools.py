from typing import List

from langchain_core.tools import tool

from src import Tech
from src.domain import SourceType
from src.sources.registry import SourceRegistry
from src.state.sub_state import RawEvent


def make_collection_tools(
    registry: SourceRegistry,
    tech: Tech,
    today: str,
    collected_events: List[RawEvent],
):
    """
    데이터 수집 도구들을 생성하는 팩토리 함수

    Args:
        registry: SourceRegistry 인스턴스
        tech: 수집할 기술 스택
        today: 오늘 날짜 (ISO 형식)
        collected_events: 수집된 이벤트를 저장할 리스트 (mutable)

    Returns:
        도구 함수들의 리스트
    """

    @tool
    def fetch_rss() -> str:
        """RSS 피드를 가져와서 최신 기술 뉴스를 수집"""
        try:
            events = registry.fetch(source=SourceType.RSS, tech=tech, today=today)
            collected_events.extend(events)
            return f"✅ Successfully fetched {len(events)} RSS feed events"
        except Exception as e:
            return f"❌ Error fetching RSS: {str(e)}"

    @tool
    def fetch_github_releases() -> str:
        """GitHub 릴리스를 가져와서 최신 버전 릴리스와 체인지로그를 수집"""
        try:
            events = registry.fetch(
                source=SourceType.GITHUB_RELEASES, tech=tech, today=today
            )
            collected_events.extend(events)
            return f"✅ Successfully fetched {len(events)} GitHub release events"
        except Exception as e:
            return f"❌ Error fetching GitHub releases: {str(e)}"

    @tool
    def search_tavily(query: str) -> str:
        """Tavily 검색을 사용하여 최근 뉴스와 업데이트를 수집

        Args:
            query: 검색 쿼리 (최근 뉴스등의 소식을 얻기 위한)
        """
        try:
            events = registry.search(
                source=SourceType.TAVILY, tech=tech, today=today, query=query
            )
            collected_events.extend(events)
            return f"✅ Successfully searched and got {len(events)} events for query: {query}"
        except Exception as e:
            return f"❌ Error searching Tavily: {str(e)}"

    @tool
    def finish_collection(reason: str) -> str:
        """여러 소스에서 충분한 원시 이벤트를 수집했을 때 호출하세요. 데이터 수집이 완료되었음을 나타내는 데 사용됩니다.

        Args:
            reason: 수집이 완료된 이유에 대한 설명
        """
        return f"✅ Collection finished: {reason}. Total events collected: {len(collected_events)}"

    return [fetch_rss, fetch_github_releases, search_tavily, finish_collection]
