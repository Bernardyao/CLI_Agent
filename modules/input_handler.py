# input_handler.py - 稳定版本
import sys
import os
from typing import Optional

def get_user_input(prompt: str = "ag> ") -> Optional[str]:
    """获取用户输入 - 稳定版本"""
    try:
        import tty
        import termios
        
        # 保存终端设置
        old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin)
        
        buffer = []
        cursor_pos = 0
        print(prompt, end="", flush=True)
        
        try:
            while True:
                char = sys.stdin.read(1)
                ascii_val = ord(char)
                
                # 回车键
                if char in ('\r', '\n'):
                    print()
                    break
                    
                # 退格键
                elif ascii_val in (127, 8):
                    if cursor_pos > 0:
                        cursor_pos -= 1
                        del buffer[cursor_pos]
                        print('\x08 \x08', end='', flush=True)
                        
                # 方向键
                elif char == '\x1b':
                    seq1 = sys.stdin.read(1)
                    seq2 = sys.stdin.read(1)
                    
                    if seq1 == '[' and seq2 == 'C':  # 右箭头
                        if cursor_pos < len(buffer):
                            cursor_pos += 1
                            print('\x1b[1C', end='', flush=True)
                    elif seq1 == '[' and seq2 == 'D':  # 左箭头
                        if cursor_pos > 0:
                            cursor_pos -= 1
                            print('\x1b[1D', end='', flush=True)
                    # 忽略其他方向键
                    
                # Ctrl+C
                elif ascii_val == 3:
                    print("^C")
                    return None
                    
                # 普通字符
                elif 32 <= ascii_val <= 126:
                    if cursor_pos == len(buffer):
                        buffer.append(char)
                        cursor_pos += 1
                        print(char, end="", flush=True)
                    else:
                        buffer.insert(cursor_pos, char)
                        cursor_pos += 1
                        # 重新显示当前行
                        current_line = ''.join(buffer)
                        print('\x1b[K' + prompt + current_line, end="")
                        # 移动光标到正确位置
                        move_cursor_to(len(prompt) + cursor_pos)
                        
        finally:
            # 恢复终端设置
            termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, old_settings)
            
        return "".join(buffer) if buffer else None
        
    except Exception:
        # 降级方案
        try:
            return input(prompt)
        except (KeyboardInterrupt, EOFError):
            return None

def move_cursor_to(col):
    """移动光标到指定列"""
    sys.stdout.write(f'\x1b[{col}G')
    sys.stdout.flush()

def get_piped_input() -> Optional[str]:
    """获取管道输入"""
    try:
        if not sys.stdin.isatty():
            content = sys.stdin.read().strip()
            return content if content else None
    except Exception:
        pass
    return None

def save_history():
    """保存历史记录"""
    pass
