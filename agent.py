# agent.py - 最终简化版主程序
from modules.input_handler import get_user_input, get_piped_input, save_history
from modules.llm_client import chat, chat_stream
from modules.utils import pretty_print
import sys

def main():
    print("★ Polar Agent CLI ")
    
    messages = [
            {"role": "system", "content": "You are a professional programming assistant,Skilled at analyzing various computer knowledge"}
    ]
    
    # 检测并处理管道输入
    piped_content = get_piped_input()
    if piped_content:
        
        user_message = {"role": "user", "content": piped_content}
        
        try:
            pretty_print("💭 Analyzing...")
            # 使用流式输出显示分析结果
            for chunk in chat_stream(messages + [user_message]):
                print(chunk, end='', flush=True)
            print("\n")
            
            # 获取完整响应用于保存
            full_response = chat(messages + [user_message])
            messages.append(user_message)
            messages.append({"role": "assistant", "content": full_response})
            save_history()
            
        except Exception as e:
            pretty_print(f"**Error:** {e}")
            return
    
    # 交互式对话循环
    while True:
        try:
            user_input = get_user_input("ag> ")
        except (KeyboardInterrupt, EOFError):
            break
            
        if user_input is None:  # Ctrl+D
            break
        if not user_input.strip():
            continue
        if user_input == "/exit":
            break

        messages.append({"role": "user", "content": user_input})

        try:
            pretty_print("Thinking...")
            # 流式输出对话
            for chunk in chat_stream(messages):
                print(chunk, end='', flush=True)
            print("\n")
            
            # 保存完整对话
            full_response = chat(messages)
            messages.append({"role": "assistant", "content": full_response})
            save_history()
            
        except Exception as e:
            pretty_print(f"**Error:** {e}")
            continue

    print("Bye!")

if __name__ == "__main__":
    main()
