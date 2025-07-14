# core/graph_state.py
"""
Defines the state and structured output models for the LangGraph agent.
"""
from typing import List, Optional, Annotated
from typing_extensions import TypedDict

from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field

class AgentState(TypedDict):
    """Defines the state passed between graph nodes."""
    messages: Annotated[List[BaseMessage], lambda x, y: x + y]
    success_criteria: str
    feedback_on_work: Optional[str]
    success_criteria_met: bool
    user_input_needed: bool

class EvaluatorOutput(BaseModel):
    """Structured output for the evaluator LLM."""
    feedback: str = Field(description="Constructive feedback on the assistant's response.")
    success_criteria_met: bool = Field(description="Whether the task's success criteria have been met.")
    user_input_needed: bool = Field(description="True if user clarification is needed or the assistant is stuck.")