"""RSS Source 플러그인 단위 테스트"""

from datetime import datetime

from dotenv import load_dotenv

from mini_agent import Tech
from mini_agent.sources.plugin.rss import RssSource
from mini_agent.types import SourceType

load_dotenv()


def test_rss_source_fetch_spring():
    """Spring RSS 피드 가져오기 테스트"""
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

    # Payload 검증
    payload = first_event["payload"]
    assert "url" in payload
    assert "feed" in payload
    assert "entries" in payload

    print(f"\n✅ RSS 피드 가져오기 성공: {len(result)}개 URL에서 데이터 수집")
    print(f"첫 번째 URL: {payload['url']}")
    print(f"엔트리 개수: {len(payload.get('entries', []))}")


def test_rss_source_fetch_nextjs():
    """Next.js RSS 피드 가져오기 테스트"""
    source = RssSource()
    today = datetime.now().strftime("%Y-%m-%d")

    result = source.fetch(tech=Tech.NEXTJS, today=today)

    assert isinstance(result, list)
    assert len(result) > 0

    print(f"\n✅ Next.js RSS 피드 가져오기 성공: {len(result)}개 URL")


def test_rss_source_no_feeds():
    """RSS 피드가 없는 기술 스택 테스트"""
    source = RssSource()
    today = datetime.now().strftime("%Y-%m-%d")

    # FastAPI는 tech_sources.py에서 RSS가 빈 리스트
    result = source.fetch(tech=Tech.FASTAPI, today=today)

    assert isinstance(result, list)
    assert len(result) == 0

    print("\n✅ RSS 피드가 없는 경우 빈 리스트 반환 확인")


def test_rss_source_payload_structure():
    """RSS 이벤트의 payload 구조 상세 검증"""
    source = RssSource()
    today = datetime.now().strftime("%Y-%m-%d")

    result = source.fetch(tech=Tech.SPRING, today=today)

    first_event = result[0]
    payload = first_event["payload"]

    # Feed 정보 확인
    feed = payload.get("feed", {})
    print("\n📰 Feed 정보:")
    print(f"  - Title: {feed.get('title', 'N/A')}")
    print(f"  - Link: {feed.get('link', 'N/A')}")

    # Entries 확인
    entries = payload.get("entries", [])
    if entries:
        first_entry = entries[0]
        print("\n📝 첫 번째 Entry:")
        print(f"  - Title: {first_entry.get('title', 'N/A')}")
        print(f"  - Link: {first_entry.get('link', 'N/A')}")
        print(f"  - Published: {first_entry.get('published', 'N/A')}")
        print(f"  - Author: {first_entry.get('author', 'N/A')}")

        # Summary 확인
        summary = first_entry.get("summary", "")
        if summary:
            print("\n  📄 Summary:")
            print(f"  {summary[:200]}...")

        # Content 확인 (HTML)
        content_list = first_entry.get("content", [])
        if content_list:
            content_html = content_list[0].get("value", "")
            print("\n  📰 Content (HTML):")
            print(f"  {content_html[:300]}...")

    assert len(entries) > 0, "엔트리가 하나 이상 있어야 합니다"
