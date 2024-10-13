from pydantic import BaseModel, Field
from typing import  Dict, Any, Callable, List

class RouteMetadata(BaseModel):
    model: str
    invoker: Callable
    capabilities: List[str] = Field(default_factory=list)
    cost: float = 0.0
    performance_score: float = 0.0
    example_sentences: List[str] = Field(default_factory=list)
    additional_info: Dict[str, Any] = Field(default_factory=dict)

class QueryResult(BaseModel):
    content: str
    metadata: RouteMetadata
