# tools/tool_loader.py
"""
Initializes and aggregates all tools for the AI assistant.
"""
import requests
from typing import List, Tuple

from langchain.agents import Tool
from langchain_community.agent_toolkits import FileManagementToolkit, PlayWrightBrowserToolkit
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_community.utilities import GoogleSerperAPIWrapper, WikipediaAPIWrapper
from langchain_experimental.tools import PythonREPLTool
from playwright.async_api import async_playwright, Browser, Playwright

import config  # Import centralized configuration

def _send_push_notification(text: str) -> str:
    """Sends a push notification via the Pushover service."""
    if not config.PUSHOVER_TOKEN or not config.PUSHOVER_USER:
        return "Pushover credentials are not configured."
    try:
        requests.post(
            "https://api.pushover.net/1/messages.json",
            data={"token": config.PUSHOVER_TOKEN, "user": config.PUSHOVER_USER, "message": text},
            timeout=10
        ).raise_for_status()
        return "Notification sent successfully."
    except requests.RequestException as e:
        return f"Failed to send notification: {e}"

async def get_all_tools() -> Tuple[List[Tool], Browser, Playwright]:
    """
    Initializes and returns all tools, the browser, and the Playwright instance.
    """
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)
    
    # Initialize toolkits
    pw_toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=browser)
    file_toolkit = FileManagementToolkit(root_dir="sandbox")

    # Define individual tools
    tools = pw_toolkit.get_tools() + file_toolkit.get_tools() + [
        Tool(
            name="web_search",
            func=GoogleSerperAPIWrapper(serper_api_key=config.SERPER_API_KEY).run,
            description="Performs a web search for up-to-date information.",
        ),
        WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper()),
        PythonREPLTool(),
        Tool(
            name="send_push_notification",
            func=_send_push_notification,
            description="Sends a push notification to the user.",
        ),
    ]
    return tools, browser, playwright