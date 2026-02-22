"""
Configuration - Environment and runtime settings.
"""

import os

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")


def validate_config() -> bool:
    """Validate that required configuration is present."""
    if not OPENAI_API_KEY or OPENAI_API_KEY == "sk-your-api-key-here":
        return False
    return True
