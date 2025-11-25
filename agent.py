# agent.py - 简化版本
from modules.input_handler import get_user_input, get_piped_input, save_history
from modules.llm_client import chat_stream
from modules.utils import safe_pretty_print
import sys

def main():
    print("★ Polar Agent CLI")
    
    messages = [
        {"role": "system", "content": "You are a professional programming assistant, Skilled at analyzing various computer knowledge"}
    ]
    
    # 检测并处理管道输入
    piped_content = get_piped_input()
    if piped_content:
        user_message = {"role": "user", "content": piped_content}
        
        try:
            print("💭 Analyzing...")
            
            # 收集完整响应
            full_response = ""
            for chunk in chat_stream(messages + [user_message]):
                if chunk:  # 确保chunk不为空
                    safe_pretty_print(chunk)  # 使用安全渲染
                    full_response += chunk
            
            print()  # 确保有换行
            
            messages.append(user_message)
            messages.append({"role": "assistant", "content": full_response})
            save_history()
            
            
        except Exception as e:
            print(f"❌ 错误: {e}")
            print("进入交互模式...")
    
    # 交互式对话循环
    while True:
        try:
            user_input = get_user_input("ag> ")
        except EOFError:
            print("Bye!")
            break
        except KeyboardInterrupt:
            print("\nBye!")
            break
        except Exception as e:
            print(f"\n输入错误: {e}, 请重试")
            continue
            
        # 处理空输入
        if not user_input or not user_input.strip():
            continue
            
        # 处理退出命令
        if user_input.strip() == "/exit":
            print("Bye!")
            break

        # 添加用户消息
        messages.append({"role": "user", "content": user_input})

        try:
            print("💭 Thinking...")
            
            # 收集完整响应
            full_response = ""
            for chunk in chat_stream(messages):
                if chunk:  # 确保chunk不为空
                    safe_pretty_print(chunk)  # 使用安全渲染
                    full_response += chunk
            
            print()  # 确保有换行
            
            messages.append({"role": "assistant", "content": full_response})
            save_history()
            
        except KeyboardInterrupt:
            print("\n^C 已中断\n")
            messages.pop()  # 移除用户消息
            continue
        except Exception as e:
            print(f"\nError: {e}\n")
            # 发生错误时移除用户消息,继续运行
            if messages and messages[-1]["role"] == "user":
                messages.pop()
            continue

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye!")
    except Exception as e:
        print(f"\n致命错误: {e}")
        sys.exit(1)
