# modules/input_handler.py

import readline
import os

HISTORY_FILE = os.path.expanduser("~/.ag_history")

# Load input history
try:
    if os.path.exists(HISTORY_FILE):
        readline.read_history_file(HISTORY_FILE)
except:
    pass

readline.set_history_length(1000)


def get_user_input(prompt="ag> "):
    """
    最小输入模块：
    - input() 提供输入
    - Ctrl+C 清行
    - Ctrl+D 返回 None（表示退出）
    - 支持历史记录（上下键）
    """
    try:
        text = input(prompt)
        text = text.strip()

        if text:
            readline.add_history(text)

        return text

    except KeyboardInterrupt:
        print("")  # 清除当前行
        return ""

    except EOFError:
        # Ctrl + D
        return None


def save_history():
    try:
        os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
        readline.write_history_file(HISTORY_FILE)
    except:
        pass

