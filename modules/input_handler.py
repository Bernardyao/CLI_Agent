# input_handler.py - 完整修复版本
import sys
from typing import Optional


def get_user_input(prompt: str = "ag> ") -> Optional[str]:
    """Simple line-based input helper for terminal use.

    - Uses the builtin input() on interactive TTY
    - Preserves KeyboardInterrupt / EOFError semantics for the caller
    - No cursor control or advanced editing to keep behavior predictable
    """
    try:
        # 非交互场景(例如被重定向/管道)统一抛 EOF,交由上层处理
        if not sys.stdin.isatty():
            raise EOFError
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        raise


def get_piped_input() -> Optional[str]:
    """Read single-shot piped input if stdin is not a TTY.

    - When stdin is a TTY, returns None
    - When stdin is redirected or piped, reads all content and strips it
    """
    if sys.stdin.isatty():
        return None

    content = sys.stdin.read()
    content = content.strip()
    return content or None


def save_history(messages=None):
    """Deprecated no-op history hook kept for backward compatibility.

    Kept only to avoid breaking older imports; current code does not
    rely on this function.
    """

    return None


