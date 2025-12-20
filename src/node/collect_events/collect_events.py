from typing import List

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from src.sources.registry import SourceRegistry
from src.state.state import GraphState
from src.state.sub_state import RawEvent
from src.tools import make_collection_tools

from .prompt import get_collection_prompt


def make_collect_events_node(registry: SourceRegistry):
    """
    Registry를 주입받아 collect_events 노드 함수 반환

    Args:
        registry: 초기화된 SourceRegistry

    Returns:
        collect_events 노드 함수
    """

    def collect_events(state: GraphState) -> GraphState:
        """
        이벤트 수집 노드 (ReAct 패턴 사용)

        - LLM 에이전트가 필요한 도구들을 선택하여 실행
        - 충분한 데이터가 모였다고 판단하면 종료
        """
        tech = state["tech"]
        today = state["today"]

        print(f"\n📡 데이터 수집 시작 (ReAct): {tech.value}")
        print(f"📅 날짜: {today}")

        # 수집된 raw events를 저장할 리스트
        collected_events: List[RawEvent] = []

        # 도구 생성
        tools = make_collection_tools(
            registry=registry,
            tech=tech,
            today=today,
            collected_events=collected_events,
        )

        # LLM 초기화
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
        )

        # ReAct 에이전트 생성
        agent_executor = create_react_agent(llm, tools)

        # 프롬프트 생성
        prompt = get_collection_prompt(tech, today)

        # 에이전트 실행
        agent_executor.invoke({"messages": [("user", prompt)]})

        print(f"\n📊 총 {len(collected_events)}개 RawEvent 수집 완료")

        return GraphState(raw_events=collected_events)

    return collect_events
