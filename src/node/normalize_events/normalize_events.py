import logging
from typing import List

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

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
    normalized_events: List[NormalizedEvent] = []

    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    agent = create_agent(
        model=model, response_format=NormalizedEvent, system_prompt=get_system_prompt()
    )

    agent.invoke(
        {
            "messages": [
                {"role": "system", "content": get_user_prompt(raw_events=raw_events)}
            ]
        }
    )

    logger.info(
        f"[normalize_events] 정규화 완료: {len(normalized_events)}개의 이벤트 생성됨"
    )

    return GraphState(events=normalized_events)
