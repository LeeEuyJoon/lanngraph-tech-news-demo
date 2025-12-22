"""normalize_events 노드 통합 테스트"""

from datetime import datetime

from dotenv import load_dotenv

from src import Tech
from src.node.normalize_events.normalize_events import normalize_events
from src.sources.plugin.github_releases import GithubReleasesSource
from src.sources.plugin.rss import RssSource
from src.sources.plugin.tavily import TavilySource
from src.state.state import GraphState

load_dotenv()


def test_normalize_events_rss() -> None:
    """normalize_events 노드 간단 테스트

    pytest tests/integration/node/test_normalize_events.py::test_normalize_events_rss -s -v
    """
    # RSS 플러그인에서 실제 데이터 1개만 가져오기
    tech = Tech.SPRING
    today = datetime.now().strftime("%Y-%m-%d")

    rss_source = RssSource()
    rss_events = rss_source.fetch(tech=tech, today=today)

    # 첫 번째 RSS 이벤트만 사용 (토큰 절약)
    raw_events = rss_events[:1] if rss_events else []

    print(f"\n📥 수집된 raw_events: {len(raw_events)}개")
    assert len(raw_events) > 0, "테스트를 위한 raw_events를 수집할 수 없습니다"

    # payload 미리보기
    if raw_events:
        payload = raw_events[0]["payload"]
        entries_count = len(payload.get("entries", []))
        print(f"   - RSS URL: {payload.get('url', 'N/A')}")
        print(f"   - Entries: {entries_count}개")

    # 상태 생성
    initial_state: GraphState = {
        "tech": tech,
        "today": today,
        "raw_events": raw_events,
    }

    # 노드 실행
    print("\n🔄 normalize_events 노드 실행 중...")
    result = normalize_events(initial_state)

    # 기본 검증
    print("\n✅ 결과 검증:")
    assert "events" in result, "result에 'events' 키가 없습니다"
    assert isinstance(result["events"], list), "events가 리스트가 아닙니다"

    events = result["events"]
    print(f"   - 정규화된 이벤트 개수: {len(events)}개")

    # 이벤트가 있으면 상세 출력
    if len(events) > 0:
        print("\n📋 정규화된 이벤트 샘플 (첫 3개):")
        for i, event in enumerate(events[:3], 1):
            print(f"\n{i}. {event.get('title', 'N/A')}")
            print(f"   소스: {event.get('source', 'N/A')}")
            print(f"   URL: {event.get('url', 'N/A')[:60]}...")
            print(f"   날짜: {event.get('published_at', 'N/A')}")
            print(f"   내용: {event.get('content', 'N/A')[:1000]}...")
    else:
        print("\n⚠️  경고: 정규화된 이벤트가 0개입니다")
        print("   이것은 normalize_events 노드가 제대로 작동하지 않았을 수 있습니다")

    print("\n" + "=" * 60)


def test_normalize_events_github() -> None:
    """normalize_events 노드 GitHub Releases 테스트

    pytest tests/integration/node/test_normalize_events.py::test_normalize_events_github -s -v
    """
    # GitHub Releases 플러그인에서 실제 데이터 1개만 가져오기
    tech = Tech.SPRING
    today = datetime.now().strftime("%Y-%m-%d")

    github_source = GithubReleasesSource()
    github_events = github_source.fetch(tech=tech, today=today)

    # 첫 번째 GitHub 이벤트만 사용
    raw_events = github_events[:1] if github_events else []

    print(f"\n📥 수집된 raw_events: {len(raw_events)}개")
    assert len(raw_events) > 0, "테스트를 위한 raw_events를 수집할 수 없습니다"

    # payload 미리보기
    if raw_events:
        payload = raw_events[0]["payload"]
        releases_count = len(payload.get("releases", []))
        print(f"   - GitHub Repo: {payload.get('repo', 'N/A')}")
        print(f"   - Releases: {releases_count}개")

    # 상태 생성
    initial_state: GraphState = {
        "tech": tech,
        "today": today,
        "raw_events": raw_events,
    }

    # 노드 실행
    print("\n🔄 normalize_events 노드 실행 중...")
    result = normalize_events(initial_state)

    # 기본 검증
    print("\n✅ 결과 검증:")
    assert "events" in result, "result에 'events' 키가 없습니다"
    assert isinstance(result["events"], list), "events가 리스트가 아닙니다"

    events = result["events"]
    print(f"   - 정규화된 이벤트 개수: {len(events)}개")

    # 이벤트가 있으면 상세 출력
    if len(events) > 0:
        print("\n📋 정규화된 이벤트 샘플 (첫 3개):")
        for i, event in enumerate(events[:3], 1):
            print(f"\n{i}. {event.get('title', 'N/A')}")
            print(f"   소스: {event.get('source', 'N/A')}")
            print(f"   URL: {event.get('url', 'N/A')[:60]}...")
            print(f"   날짜: {event.get('published_at', 'N/A')}")
            content = event.get("content", "N/A")
            print(f"   내용 길이: {len(content)}자")
            print(f"   내용: {content[:1000]}...")
    else:
        print("\n⚠️  경고: 정규화된 이벤트가 0개입니다")
        print("   이것은 normalize_events 노드가 제대로 작동하지 않았을 수 있습니다")

    print("\n" + "=" * 60)


def test_normalize_events_tavily() -> None:
    """normalize_events 노드 Tavily 테스트

    pytest tests/integration/node/test_normalize_events.py::test_normalize_events_tavily -s -v
    """
    # Tavily 플러그인에서 실제 데이터 가져오기
    tech = Tech.SPRING
    today = datetime.now().strftime("%Y-%m-%d")

    tavily_source = TavilySource()
    # Tavily search는 쿼리가 필요
    tavily_events = tavily_source.search(
        tech=tech, today=today, query="Spring Boot 3 latest updates"
    )

    # Tavily는 항상 1개의 RawEvent 반환 (쿼리당 1개)
    raw_events = tavily_events[:1] if tavily_events else []

    print(f"\n📥 수집된 raw_events: {len(raw_events)}개")
    assert len(raw_events) > 0, "테스트를 위한 raw_events를 수집할 수 없습니다"

    # payload 미리보기
    if raw_events:
        payload = raw_events[0]["payload"]
        results_count = len(payload.get("results", []))
        print(f"   - Tavily Query: {payload.get('query', 'N/A')}")
        print(f"   - Search Results: {results_count}개")

    # 상태 생성
    initial_state: GraphState = {
        "tech": tech,
        "today": today,
        "raw_events": raw_events,
    }

    # 노드 실행
    print("\n🔄 normalize_events 노드 실행 중...")
    result = normalize_events(initial_state)

    # 기본 검증
    print("\n✅ 결과 검증:")
    assert "events" in result, "result에 'events' 키가 없습니다"
    assert isinstance(result["events"], list), "events가 리스트가 아닙니다"

    events = result["events"]
    print(f"   - 정규화된 이벤트 개수: {len(events)}개")

    # 이벤트가 있으면 상세 출력
    if len(events) > 0:
        print("\n📋 정규화된 이벤트 샘플 (첫 3개):")
        for i, event in enumerate(events[:3], 1):
            print(f"\n{i}. {event.get('title', 'N/A')}")
            print(f"   소스: {event.get('source', 'N/A')}")
            print(f"   URL: {event.get('url', 'N/A')[:60]}...")
            print(f"   날짜: {event.get('published_at', 'N/A')}")
            content = event.get("content", "N/A")
            print(f"   내용 길이: {len(content)}자")
            print(f"   내용: {content[:500]}...")
    else:
        print("\n⚠️  경고: 정규화된 이벤트가 0개입니다")
        print("   이것은 normalize_events 노드가 제대로 작동하지 않았을 수 있습니다")

    print("\n" + "=" * 60)
