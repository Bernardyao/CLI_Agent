# modules/llm_client.py

import requests
import json
from config import API_KEY, BASE_URL, MODEL


def chat(messages):
    """
    非流式，最小请求逻辑
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": messages
    }

    response = requests.post(BASE_URL, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()

    return data["choices"][0]["message"]["content"]

