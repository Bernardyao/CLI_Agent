# agent.py - 完整修复版
from modules.input_handler import get_user_input, get_piped_input, save_history
from modules.llm_client import chat_stream
from modules.utils import pretty_print
import sys

def main():
    print("★ Polar Agent CLI ")
    
    messages = [
        {"role": "system", "content": "You are a professional programming assistant, Skilled at analyzing various computer knowledge"}
    ]
    
    # 检测并处理管道输入
    piped_content = get_piped_input()
    if piped_content:
        user_message = {"role": "user", "content": piped_content}
        
        try:
            print("💭 Analyzing...\n")
            
            # 在流式输出时收集完整响应,避免双重API调用
            full_response = ""
            for chunk in chat_stream(messages + [user_message]):
                print(chunk, end='', flush=True)
                full_response += chunk
            print("\n")
            
            messages.append(user_message)
            messages.append({"role": "assistant", "content": full_response})
            save_history()
            
        except Exception as e:
            print(f"Error: {e}")
            print("\n进入交互模式...\n")
    
    # 交互式对话循环
    while True:
        try:
            user_input = get_user_input("ag> ")
        except EOFError:
            # Ctrl+D 退出
            print("Bye!")
            break
        except KeyboardInterrupt:
            # Ctrl+C 退出
            print("\nBye!")
            break
        except Exception as e:
            # 其他输入错误,继续循环
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
            print("Thinking...\n")
            
            # 在流式输出时收集完整响应,避免双重API调用
            full_response = ""
            for chunk in chat_stream(messages):
                print(chunk, end='', flush=True)
                full_response += chunk
            print("\n")
            
            # 直接使用收集到的响应,不再调用chat()
            messages.append({"role": "assistant", "content": full_response})
            save_history()
            
        except KeyboardInterrupt:
            # Ctrl+C时移除未完成的消息,继续运行
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

