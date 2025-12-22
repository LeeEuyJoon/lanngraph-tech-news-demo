"""RSS Source 플러그인 단위 테스트"""

from datetime import datetime

from dotenv import load_dotenv

from src import Tech
from src.domain import SourceType
from src.sources.plugin.rss import RssSource

load_dotenv()


def test_rss_source_fetch_spring():
    """Spring RSS 피드 가져오기 테스트

    pytest tests/unit/sources/test_rss_source.py -s -v
    """
    source = RssSource()
    today = datetime.now().strftime("%Y-%m-%d")

    result = source.fetch(tech=Tech.SPRING, today=today)

    # 결과 검증
    assert isinstance(result, list)
    assert len(result) > 0

    # 첫 번째 이벤트 검증
    first_event = result[0]
    assert first_event["source"] == SourceType.RSS
    assert "fetched_at" in first_event
    assert "payload" in first_event

    # Payload 검증 (최적화된 구조)
    payload = first_event["payload"]
    assert "url" in payload
    assert "entries" in payload

    print(f"\n{len(result)}개 URL에서 데이터 수집")
    print(f"첫 번째 URL: {payload['url']}")
    print(f"엔트리 개수: {len(payload.get('entries', []))}")


def test_rss_source_fetch_nextjs():
    """Next.js RSS 피드 가져오기 테스트"""
    source = RssSource()
    today = datetime.now().strftime("%Y-%m-%d")

    result = source.fetch(tech=Tech.NEXTJS, today=today)

    assert isinstance(result, list)
    assert len(result) > 0

    print(f"\n{len(result)}개 URL")


def test_rss_source_no_feeds():
    """RSS 피드가 없는 기술 스택 테스트"""
    source = RssSource()
    today = datetime.now().strftime("%Y-%m-%d")

    # FastAPI는 tech_sources.py에서 RSS가 빈 리스트
    result = source.fetch(tech=Tech.FASTAPI, today=today)

    assert isinstance(result, list)
    assert len(result) == 0

    print("\nRSS 피드가 없는 경우 빈 리스트 반환 확인")


def test_rss_source_payload_structure():
    """RSS 이벤트의 payload 구조 상세 검증 (최적화된 구조)"""
    source = RssSource()
    today = datetime.now().strftime("%Y-%m-%d")

    result = source.fetch(tech=Tech.SPRING, today=today)

    first_event = result[0]
    payload = first_event["payload"]

    # 최적화된 구조에서는 feed 정보가 제거됨
    print("\n📰 Payload 정보:")
    print(f"  - URL: {payload.get('url', 'N/A')}")

    # Entries 확인 (simplified_entries)
    entries = payload.get("entries", [])
    assert len(entries) > 0, "엔트리가 하나 이상 있어야 합니다"

    if entries:
        first_entry = entries[0]
        print("\n📝 첫 번째 Entry (최적화된 필드):")
        print(f"  - Title: {first_entry.get('title', 'N/A')}")
        print(f"  - Link: {first_entry.get('link', 'N/A')}")
        print(f"  - Published: {first_entry.get('published', 'N/A')}")
        print(f"  - Author: {first_entry.get('author', 'N/A')}")

        # Summary 확인
        summary = first_entry.get("summary", "")
        if summary:
            print("\n  📄 Summary:")
            print(f"  {summary[:200]}...")

        # Content 확인
        content = first_entry.get("content", "")
        if content:
            print("\n  📰 Content:")
            print(f"  {content[:300]}...")

        # 최적화된 구조 검증: 필수 필드만 있는지 확인
        assert "title" in first_entry
        assert "link" in first_entry
        assert "published" in first_entry
        assert "summary" in first_entry
        assert "content" in first_entry
        assert "author" in first_entry
