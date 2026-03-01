from typing import TypedDict, Optional, List
from langgraph.graph import add_messages

class AgentState(TypedDict):
    original_prompt: str
    optimized_prompt: Optional[str]
    generated_image_url: Optional[str]
    critique: Optional[str]
    iteration_count: int
    quality_score: float
    status: str
    max_iterations: int
    messages: List[str] # for tracking steps
