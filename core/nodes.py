# core/nodes.py
"""
Defines the functions (nodes) that constitute the agent's graph.
"""
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from . import prompts
from .graph_state import AgentState, EvaluatorOutput
import config

def worker_node(state: AgentState, worker_llm_with_tools: ChatOpenAI) -> Dict[str, Any]:
    """Executes the primary task using the worker LLM."""
    system_prompt = prompts.get_worker_prompt(state)
    messages = state["messages"]

    if messages and isinstance(messages[0], SystemMessage):
        messages[0] = SystemMessage(content=system_prompt)
    else:
        messages.insert(0, SystemMessage(content=system_prompt))
    
    response = worker_llm_with_tools.invoke(messages)
    return {"messages": [response]}

def evaluator_node(state: AgentState, evaluator_llm: ChatOpenAI) -> Dict[str, Any]:
    """Assesses the worker's output against the success criteria."""
    evaluator_prompt = prompts.get_evaluator_prompt(state)
    messages = [
        SystemMessage(content="You are an expert evaluator."),
        HumanMessage(content=evaluator_prompt)
    ]
    
    eval_result: EvaluatorOutput = evaluator_llm.invoke(messages)
    
    return {
        "feedback_on_work": eval_result.feedback,
        "success_criteria_met": eval_result.success_criteria_met,
        "user_input_needed": eval_result.user_input_needed
    }