import logging
from typing import List, cast

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from src.state.schemas import NormalizedEvents
from src.state.state import GraphState
from src.state.sub_state import NormalizedEvent

from .prompt import get_system_prompt, get_user_prompt

logger = logging.getLogger(__name__)


def normalize_events(state: GraphState) -> GraphState:
    """
    이벤트 일반화 노드

    - 수집된 raw events를 정규화하여 일관된 형식으로 변환
    """

    raw_events = state["raw_events"]

    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    agent = create_agent(
        model=model, response_format=NormalizedEvents, system_prompt=get_system_prompt()
    )

    result = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": get_user_prompt(raw_events=raw_events)}
            ]
        }
    )

    structured = result.get("structured_response")
    if not structured:
        logger.error("[normalize_events] 정규화 실패: 구조화된 응답이 없습니다")
        return GraphState(events=[])

    structured = cast(NormalizedEvents, structured)
    events: List[NormalizedEvent] = structured.get("events", [])

    logger.info(f"[normalize_events] 정규화 완료: {len(events)}개의 이벤트 생성됨")

    return GraphState(events=events)
