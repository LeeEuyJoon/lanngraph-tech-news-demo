from typing import Any, Dict, List

from pydantic import BaseModel, Field


class CollectionPlanItemModel(BaseModel):
    source: str = Field(..., description="registry key")
    config: Dict[str, Any] = Field(default_factory=dict)


class CollectionPlan(BaseModel):
    plans: List[CollectionPlanItemModel]
