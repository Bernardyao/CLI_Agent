# modules/llm_client.py - 最终版
import json
from typing import List, Dict, Iterator

import requests

from config import BASE_URL, MODEL, ensure_api_key


def _build_headers() -> Dict[str, str]:
    api_key = ensure_api_key()
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def chat(messages: List[Dict[str, str]], **kwargs) -> str:
    """Non-streaming chat helper (keeps original interface)."""
    headers = _build_headers()
    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": kwargs.get("temperature", 0.7),
        "max_tokens": kwargs.get("max_tokens", 2048),
    }

    response = requests.post(BASE_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()

    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        raise RuntimeError(
            f"Unexpected LLM response format: {json.dumps(data, ensure_ascii=False)[:500]}"
        )


def chat_stream(messages: List[Dict[str, str]], **kwargs) -> Iterator[str]:
    """Streaming chat helper.

    Keeps the same external interface while adding API key validation and
    more robust parsing of the streamed responses.
    """
    headers = _build_headers()
    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": kwargs.get("temperature", 0.7),
        "max_tokens": kwargs.get("max_tokens", 2048),
        "stream": True,
    }

    response = requests.post(
        BASE_URL,
        headers=headers,
        json=payload,
        stream=True,
        timeout=60,
    )
    response.raise_for_status()

    for line in response.iter_lines():
        if not line:
            continue

        line = line.decode("utf-8")
        if not line.startswith("data: "):
            continue

        data_str = line[6:]
        if data_str.strip() == "[DONE]":
            break

        try:
            data = json.loads(data_str)
        except json.JSONDecodeError:
            continue

        choices = data.get("choices") or []
        if not choices:
            continue

        delta = choices[0].get("delta") or {}
        content = delta.get("content")
        if content:
            yield content
