# agent.py

from modules.input_handler import get_user_input, save_history
from modules.llm_client import chat
from modules.utils import pretty_print

def main():
    print("Polaris Agent CLI")

    messages = [
            {"role": "system", "content": "You are a helpful CLI assistant,major in computer science."}
    ]

    while True:
        user_input = get_user_input("ag> ")

        if user_input is None:   # Ctrl+D
            break

        if not user_input:
            continue

        if user_input == "/exit":
            break

        messages.append({"role": "user", "content": user_input})

        try:
            reply = chat(messages)
        except Exception as e:
            pretty_print(f"**Error:** {e}")
            continue

        messages.append({"role": "assistant", "content": reply})
        pretty_print(reply)

    save_history()
    print("Bye!")


if __name__ == "__main__":
    main()

