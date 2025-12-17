from typing import Any, List, TypedDict

from ..types import SourceType


class CollectionPlanItem(TypedDict, total=False):
    source: SourceType
    rss_urls: List[str]
    github_repos: List[str]
    web_search_queries: List[str]


class RawEvent(TypedDict):
    source: SourceType
    fetched_at: str  # ISO
    payload: Any  # rss xml str / github json / search json


class NormalizedEvent(TypedDict, total=True):
    source: SourceType
    title: str
    url: str
    published_at: str  # ISO
    content: str  # plain text or html


class Evaluation(TypedDict, total=False):
    pass_: bool  # `pass`는 키워드라 pass_ 추천
    feedback: str
