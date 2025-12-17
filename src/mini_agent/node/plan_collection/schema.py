from typing import List, Literal

from pydantic import BaseModel, Field


class CollectionPlanItemModel(BaseModel):
    source: Literal["github_releases", "rss", "tavily"]
    rss_urls: List[str] = Field(default_factory=list)
    github_repos: List[str] = Field(default_factory=list)
    web_search_queries: List[str] = Field(default_factory=list)


class CollectionPlan(BaseModel):
    """LLM structured output용 수집 계획 리스트 래퍼"""

    plans: List[CollectionPlanItemModel] = Field(..., description="수집 계획 리스트")
