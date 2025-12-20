import logging
from typing import List

# from langgraph.prebuilt import create_react_agent
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.graph.state import CompiledStateGraph

from src.sources.registry import SourceRegistry
from src.state.state import GraphState
from src.state.sub_state import RawEvent
from src.tools import make_collection_tools
from src.utils.logging import log_node_execution

from .prompt import get_system_prompt, get_user_prompt

logger = logging.getLogger(__name__)


def make_collect_events_node(registry: SourceRegistry):
    """
    Registry를 주입받아 collect_events 노드 함수 반환

    Args:
        registry: 초기화된 SourceRegistry

    Returns:
        collect_events 노드 함수
    """

    @log_node_execution
    def collect_events(state: GraphState) -> GraphState:
        """
        이벤트 수집 노드 (ReAct 패턴 사용)

        - LLM 에이전트가 필요한 도구들을 선택하여 실행
        - 충분한 데이터가 모였다고 판단하면 종료
        """
        tech = state["tech"]
        today = state["today"]

        logger.info(f"[collect_events] 데이터 수집 시작: {tech.value}")

        # 수집된 raw events를 저장할 리스트
        collected_events: List[RawEvent] = []

        # 도구 생성
        tools = make_collection_tools(
            registry=registry,
            tech=tech,
            today=today,
            collected_events=collected_events,
        )

        model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

        # ReAct 에이전트 생성
        agent: CompiledStateGraph = create_agent(
            model=model,
            tools=tools,
            system_prompt=get_system_prompt(tech, today),
        )

        # 에이전트 실행
        agent.invoke({"messages": [{"role": "user", "content": get_user_prompt()}]})

        logger.info(
            f"[collect_events] 데이터 수집 완료: {len(collected_events)}개 이벤트 수집됨"
        )

        # 수집된 이벤트 반환
        for event in collected_events:
            playlaod_preview = str(event["payload"])[:50]
            logger.info(
                f"[collect_events] 수집된 이벤트: {event['source']}: {playlaod_preview}..."
            )

        return GraphState(raw_events=collected_events)

    return collect_events
