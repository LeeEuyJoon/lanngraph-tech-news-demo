from typing import Any, Dict, TypedDict

from ..types import SourceType


class CollectionPlanItem(TypedDict):
    source: str
    config: Dict[str, Any]


class RawEvent(TypedDict):
    source: str
    fetched_at: str  # ISO
    payload: Any  # rss xml str / github json / search json


class NormalizedEvent(TypedDict, total=False):
    source: SourceType
    title: str
    url: str
    published_at: str  # ISO
    content: str  # plain text or html


class Evaluation(TypedDict, total=False):
    pass_: bool  # `pass`는 키워드라 pass_ 추천
    feedback: str
