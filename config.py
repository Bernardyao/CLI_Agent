# config.py
import os

# API configuration
API_KEY = os.getenv("QNAI_API_KEY")  # Read from environment
BASE_URL = "https://api.qnaigc.com/v1/chat/completions"
MODEL = "deepseek/deepseek-v3.1-terminus"  # Keep in sync with README


def ensure_api_key() -> str:
    """Ensure API key is available at runtime, otherwise raise a clear error.

    Called only right before sending a request so import does not fail early.
    """

    key = API_KEY or os.getenv("QNAI_API_KEY")
    if not key:
        raise RuntimeError(
            "QNAI_API_KEY is not set. Please configure it in your environment before running CLI_Agent."
        )
    return key




