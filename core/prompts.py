# core/prompts.py
"""
Contains all prompt templates used by the worker and evaluator nodes.
"""
from datetime import datetime
from .graph_state import AgentState

def get_worker_prompt(state: AgentState) -> str:
    """Constructs the system prompt for the worker agent."""
    prompt = f"""You are a helpful AI assistant with access to a rich set of tools.
                The current date and time is {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.

                Your goal is to complete the user's request by meeting the following success criteria:
                "{state['success_criteria']}"

                Work autonomously until you either meet the criteria or require clarification from the user.
                - If you have a question, state it clearly (e.g., "Question: Do you need a summary or a detailed report?").
                - If you have completed the task, provide the final answer directly.
            """
    if state.get("feedback_on_work"):
        prompt += f"""
                    ---
                    PREVIOUS ATTEMPT FEEDBACK:
                    You received the following feedback on a prior attempt. Use it to improve your work:
                    "{state['feedback_on_work']}"
                """
    return prompt

def get_evaluator_prompt(state: AgentState) -> str:
    """Constructs the user-facing message for the evaluator."""
    conversation_history = "\n".join(
        f"{msg.type.capitalize()}: {msg.content}" for msg in state['messages']
    )
    
    return f"""You are an impartial evaluator assessing an AI assistant's work.
                Your task is to determine if the assistant's latest response fulfills the user's request based on the provided criteria.

                **Conversation History:**
                {conversation_history}

                **Success Criteria:**
                "{state['success_criteria']}"

                **Assistant's Final Response to Evaluate:**
                "{state['messages'][-1].content}"

                **Your Tasks:**
                1. Provide constructive feedback on the response.
                2. Decide if the response meets the success criteria.
                3. Determine if user input is now required.
            """