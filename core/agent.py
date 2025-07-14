# core/agent.py
"""
The main Sidekick agent class that orchestrates all components.
"""
import uuid
from typing import List, Dict

from langchain_core.messages import HumanMessage, AIMessage

from tools.tool_loader import get_all_tools
from .graph_builder import build_graph

class Sidekick:
    """Manages the lifecycle, graph, and execution of the AI assistant."""

    def __init__(self):
        self.sidekick_id = str(uuid.uuid4())
        self.tools = []
        self.browser = None
        self.playwright = None
        self.graph = None

    async def setup(self):
        """Initializes all components of the Sidekick."""
        print("Setting up Sidekick...")
        self.tools, self.browser, self.playwright = await get_all_tools()
        self.graph = build_graph(self.tools)
        print("Sidekick setup complete.")

    async def run_step(self, message_history: List[Dict], success_criteria: str) -> List[Dict]:
        """Runs a single step of the graph execution."""
        config = {"configurable": {"thread_id": self.sidekick_id}}
        initial_state = {
            "messages": [HumanMessage(content=message_history[-1]["content"])],
            "success_criteria": success_criteria or "The answer is clear, concise, and accurate.",
        }

        final_state = await self.graph.ainvoke(initial_state, config=config)

        last_ai_message = next((msg for msg in reversed(final_state.get("messages", [])) if isinstance(msg, AIMessage)), None)
        response_content = last_ai_message.content if last_ai_message else "No final response was generated."

        return [
            *message_history,
            {"role": "assistant", "content": response_content},
            {"role": "assistant", "content": f"Evaluator Feedback: {final_state['feedback_on_work']}"},
        ]

    async def cleanup(self):
        """Gracefully closes resources."""
        print("Cleaning up Sidekick resources...")
        if self.browser: await self.browser.close()
        if self.playwright: await self.playwright.stop()
        print("Cleanup complete.")