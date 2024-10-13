from pydantic import BaseModel, Field
from typing import  Dict, Any, Callable, List

class RouteMetadata(BaseModel):
    model: str
    invoker: Callable = Field(..., exclude=True)
    capabilities: List[str]
    cost: float
    performance_score: float
    example_sentences: List[str]
    additional_info: Dict[str, Any] = {}

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            Callable: lambda v: v.__name__,
            list: lambda v: ', '.join(str(i) for i in v),
            dict: lambda v: str(v)
        }
        extra = 'allow'

class QueryResult(BaseModel):
    content: str
    metadata: RouteMetadata
