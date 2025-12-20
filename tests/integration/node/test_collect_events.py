"""collect_events 노드 통합 테스트"""

from datetime import datetime

from dotenv import load_dotenv

from src import Tech
from src.domain import SourceType
from src.node.collect_events.collect_events import make_collect_events_node
from src.sources.plugin.github_releases import GithubReleasesSource
from src.sources.plugin.rss import RssSource
from src.sources.plugin.tavily import TavilySource
from src.sources.registry import build_default_registry
from src.state.state import GraphState

load_dotenv()  # 환경 변수 로드


def test_collect_events_integration():
    """collect_events 노드 테스트

    pytest tests/integration/node/test_collect_events.py -s -v
    """
    # Given: 실제 Registry 구성
    registry = build_default_registry(
        [
            RssSource(),
            GithubReleasesSource(),
            TavilySource(),
        ]
    )

    node_fn = make_collect_events_node(registry)

    initial_state: GraphState = {
        "tech": Tech.SPRING,
        "today": datetime.now().strftime("%Y-%m-%d"),
    }

    # 노드 실행
    result = node_fn(initial_state)

    # 검증: raw_events 필드가 존재하는지
    assert "raw_events" in result
    assert isinstance(result["raw_events"], list)

    # 검증: 최소 한 개 이상의 이벤트가 수집되었는지
    assert len(result["raw_events"]) > 0, "수집된 이벤트가 없습니다"

    # 검증: 수집된 이벤트들이 올바른 타입인지
    for event in result["raw_events"]:
        assert "source" in event
        assert "fetched_at" in event
        assert "payload" in event
        assert event["source"] in [
            SourceType.RSS,
            SourceType.GITHUB_RELEASES,
            SourceType.TAVILY,
        ]

    sources = {event["source"] for event in result["raw_events"]}
    assert len(sources) >= 2, f"최소 2개 소스 필요, 현재: {sources}"

    # 결과 출력
    print("\n" + "=" * 60)
    print("=" * 60)
    print(f"📊 총 수집 이벤트: {len(result['raw_events'])}개")
    print(f"📡 사용된 소스: {len(sources)}개")
    print()

    for i, event in enumerate(result["raw_events"], 1):
        source = event["source"].value
        payload_str = str(event["payload"])[:50]
        print(f"{i}. [{source}] {payload_str}...")

    print("=" * 60)
