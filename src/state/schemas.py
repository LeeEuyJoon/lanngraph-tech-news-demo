from typing import List, TypedDict

from .sub_state import NormalizedEvent


class NormalizedEvents(TypedDict):
    events: List[NormalizedEvent]
