# core/graph_builder.py
"""
Constructs and compiles the LangGraph for the AI Sidekick.
"""
from functools import partial
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

from .graph_state import AgentState, EvaluatorOutput
from . import nodes
import config

# --- Router Functions ---
def worker_router(state: AgentState) -> str:
    """Routes from worker to tools or evaluator."""
    last_message = state["messages"][-1]
    return "tools" if hasattr(last_message, "tool_calls") and last_message.tool_calls else "evaluator"

def route_after_evaluation(state: AgentState) -> str:
    """Routes to end or back to worker after evaluation."""
    return "end" if state["success_criteria_met"] or state["user_input_needed"] else "worker"

# --- Graph Construction ---
def build_graph(tools: list) -> StateGraph:
    """Builds and returns the compiled LangGraph."""
    # Initialize LLMs for nodes
    worker_llm = ChatOpenAI(model=config.WORKER_MODEL).bind_tools(tools)
    evaluator_llm = ChatOpenAI(model=config.EVALUATOR_MODEL).with_structured_output(EvaluatorOutput)
    
    # Bind LLMs to their respective nodes
    bound_worker_node = partial(nodes.worker_node, worker_llm_with_tools=worker_llm)
    bound_evaluator_node = partial(nodes.evaluator_node, evaluator_llm=evaluator_llm)

    graph_builder = StateGraph(AgentState)
    
    # Add nodes
    graph_builder.add_node("worker", bound_worker_node)
    graph_builder.add_node("tools", ToolNode(tools))
    graph_builder.add_node("evaluator", bound_evaluator_node)
    
    # Add edges
    graph_builder.add_edge(START, "worker")
    graph_builder.add_conditional_edges("worker", worker_router, {"tools": "tools", "evaluator": "evaluator"})
    graph_builder.add_edge("tools", "worker")
    graph_builder.add_conditional_edges("evaluator", route_after_evaluation, {"worker": "worker", "end": END})
    
    return graph_builder.compile(checkpointer=MemorySaver())