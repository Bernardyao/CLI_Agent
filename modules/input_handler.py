# input_handler.py - 完整修复版本
import sys
import os
from typing import Optional

def get_user_input(prompt: str = "ag> ") -> Optional[str]:
    """获取用户输入 - 完整修复版本"""
    try:
        import tty
        import termios
        
        # 检查stdin是否可用
        if not sys.stdin.isatty():
            # 如果stdin不是终端,使用input降级
            return input(prompt)
        
        # 保存终端设置
        old_settings = termios.tcgetattr(sys.stdin)
        
        try:
            tty.setcbreak(sys.stdin)
            
            buffer = []
            cursor_pos = 0
            print(prompt, end="", flush=True)
            
            while True:
                try:
                    char = sys.stdin.read(1)
                    if not char:  # EOF
                        raise EOFError
                    ascii_val = ord(char)
                except:
                    raise EOFError
                
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
                    try:
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
                    except:
                        pass
                    
                # Ctrl+C
                elif ascii_val == 3:
                    print("^C")
                    raise KeyboardInterrupt
                    
                # Ctrl+D - 处理EOF
                elif ascii_val == 4:
                    if not buffer:  # 空行时Ctrl+D才退出
                        print()
                        raise EOFError
                    # 否则忽略
                    
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
                        print('\r\x1b[K' + prompt + current_line, end="", flush=True)
                        # 移动光标到正确位置
                        move_cursor_to(len(prompt) + cursor_pos)
                        
        finally:
            # 确保终端设置一定会恢复
            try:
                termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, old_settings)
            except:
                pass
        
        return "".join(buffer) if buffer else ""
        
    except (KeyboardInterrupt, EOFError):
        # 重新抛出,让上层处理
        raise
    except Exception as e:
        # 降级方案:使用标准input
        try:
            return input(prompt)
        except (KeyboardInterrupt, EOFError):
            raise
        except Exception:
            return ""

def move_cursor_to(col):
    """移动光标到指定列"""
    sys.stdout.write(f'\x1b[{col}G')
    sys.stdout.flush()

def get_piped_input() -> Optional[str]:
    """获取管道输入 - 完全重写"""
    try:
        # 检查是否有管道输入
        if not sys.stdin.isatty():
            content = sys.stdin.read().strip()
            
            # ✅ 关键修复:重新打开stdin到终端
            sys.stdin.close()
            sys.stdin = open('/dev/tty', 'r')
            
            return content if content else None
    except Exception as e:
        # 如果无法重新打开tty,尝试其他方式
        try:
            # 在某些环境下,尝试重新绑定到标准输入
            import io
            sys.stdin = io.TextIOWrapper(
                os.fdopen(0, 'rb', buffering=0), 
                encoding='utf-8',
                line_buffering=True
            )
        except:
            pass
    return None

def save_history():
    """保存历史记录"""
    pass


