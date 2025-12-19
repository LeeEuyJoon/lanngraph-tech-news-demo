import operator
from typing import Annotated, List, TypedDict

from ..sources import Tech
from .sub_state import (
    CollectionPlanItem,
    Evaluation,
    NormalizedEvent,
    RawEvent,
)


class GraphState(TypedDict, total=False):
    # input
    tech: Tech

    # loop control
    attempt: int
    max_attempts: int

    # planning
    collection_plan: List[CollectionPlanItem]

    # Today (ISO format: YYYY-MM-DD)
    today: str

    # execution artifacts
    raw_events: List[RawEvent]
    events: Annotated[List[NormalizedEvent], operator.add]

    # evaluation / output
    evaluation: Evaluation
    final_answer: str

    # error
    errors: Annotated[List[str], operator.add]
