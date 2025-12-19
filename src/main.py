from datetime import datetime

from dotenv import load_dotenv
from langgraph.graph import StateGraph

from src import Tech
from src.node.collect_events.collect_events import make_collect_events_node
from src.sources.plugin.github_releases import GithubReleasesSource
from src.sources.plugin.rss import RssSource
from src.sources.plugin.tavily import TavilySource
from src.sources.registry import build_default_registry
from src.state.state import GraphState

load_dotenv()


def build_graph():
    """LangGraph 그래프 구성 및 반환"""

    # Registry 초기화
    registry = build_default_registry(
        [
            RssSource(),
            GithubReleasesSource(),
            TavilySource(),
        ]
    )

    # SateGpraph 초기화
    graph = StateGraph(GraphState)

    # 노드 추가
    collect_events = make_collect_events_node(registry)
    graph.add_node("collect_events", collect_events)

    # 엣지 추가
    graph.set_entry_point("collect_events")
    graph.set_finish_point("collect_events")

    # 그래프 컴파일
    return graph.compile()


def run(tech: Tech, max_attempts: int = 3):
    app = build_graph()

    initial_state: GraphState = {
        "tech": tech,
        "today": datetime.now().strftime("%Y-%m-%d"),
        "attempt": 0,
        "max_attempts": max_attempts,
    }

    # 실행
    print(f"🚀 Tech News Agent 시작: {tech.value}")
    print(f"📅 날짜: {initial_state['today']}")
    print("-" * 50)

    result = app.invoke(initial_state)

    print("-" * 50)
    return result


if __name__ == "__main__":
    # 예제 실행
    result = run(Tech.SPRING)
    print(f"\n📊 결과: {result}")
