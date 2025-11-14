# modules/llm_client.py - 最终版
import requests
import json
import time
from typing import List, Dict, Any, Iterator

def chat(messages: List[Dict[str, str]], **kwargs) -> str:
    """非流式聊天（保持原有功能）"""
    from config import API_KEY, BASE_URL, MODEL
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": kwargs.get('temperature', 0.7),
        "max_tokens": kwargs.get('max_tokens', 2048)
    }
    
    response = requests.post(BASE_URL, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]

def chat_stream(messages: List[Dict[str, str]], **kwargs) -> Iterator[str]:
    """流式聊天（新功能）"""
    from config import API_KEY, BASE_URL, MODEL
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": kwargs.get('temperature', 0.7),
        "max_tokens": kwargs.get('max_tokens', 2048),
        "stream": True  # 启用流式
    }
    
    try:
        response = requests.post(BASE_URL, headers=headers, json=payload, stream=True, timeout=60)
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    data_str = line[6:]  # 移除 "data: " 前缀
                    if data_str.strip() == '[DONE]':
                        break
                    try:
                        data = json.loads(data_str)
                        if 'choices' in data and data['choices']:
                            delta = data['choices'][0].get('delta', {})
                            if 'content' in delta:
                                yield delta['content']
                    except json.JSONDecodeError:
                        continue
                        
    except requests.exceptions.RequestException as e:
        yield f"❌ 网络错误: {str(e)}"
    except Exception as e:
        yield f"❌ 处理错误: {str(e)}"
