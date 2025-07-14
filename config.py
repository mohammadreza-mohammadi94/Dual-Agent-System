# config.py
"""
Centralized configuration management for the AI Sidekick project.

Loads environment variables and defines constants for model names, API keys,
and other settings to be used across the application.
"""
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv(override=True)

# --- LLM Models ---
WORKER_MODEL = "gpt-4o-mini"
EVALUATOR_MODEL = "gpt-4o-mini"

# --- LangSmith Tracing ---
# To enable tracing, set LANGCHAIN_TRACING_V2 to "true"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API_KEY", "")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "AI Sidekick - Modular")

# --- Pushover Notifications ---
PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN")
PUSHOVER_USER = os.getenv("PUSHOVER_USER")

# --- Serper API Key ---
SERPER_API_KEY = os.getenv("SERPER_API_KEY")