# agent.py - 简化版本
import sys
from modules.input_handler import get_user_input, get_piped_input
from modules.llm_client import chat_stream
from modules.utils import safe_pretty_print


def main() -> None:
    print("★ Polar Agent CLI")

    messages = [
        {
            "role": "system",
            "content": "You are a professional programming assistant. Be concise, accurate and helpful.",
        }
    ]

    # First, check for piped input. If present, handle one-shot and exit (script-friendly).
    piped_content = get_piped_input()
    if piped_content:
        user_message = {"role": "user", "content": piped_content}

        try:
            print("💭 Analyzing...")

            full_response = ""
            for chunk in chat_stream(messages + [user_message]):
                if chunk:
                    safe_pretty_print(chunk)
                    full_response += chunk

            print()

            messages.append(user_message)
            messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            print(f"Error in piped mode: {e}")

        print("Bye!")
        return

    # If there is no piped input but we have CLI arguments, treat them
    # as an initial question before entering interactive mode.
    if len(sys.argv) > 1:
        initial_question = " ".join(sys.argv[1:]).strip()
        if initial_question:
            user_message = {"role": "user", "content": initial_question}
            messages.append(user_message)

            try:
                print("💭 Thinking...")

                full_response = ""
                for chunk in chat_stream(messages):
                    if chunk:
                        safe_pretty_print(chunk)
                        full_response += chunk

                print()

                messages.append({"role": "assistant", "content": full_response})

            except Exception as e:
                print(f"\nError: {e}\n")
                if messages and messages[-1]["role"] == "user":
                    messages.pop()

    # Interactive conversation loop; exit only on explicit command or Ctrl+C/EOF
    while True:
        try:
            user_input = get_user_input("ag> ")
        except EOFError:
            print("\nBye!")
            break
        except KeyboardInterrupt:
            print("\nBye!")
            break
        except Exception as e:
            print(f"\nInput error: {e}, please try again")
            continue

        if not user_input or not user_input.strip():
            continue

        cmd = user_input.strip()

        # Exit commands
        if cmd in {"/exit", "/quit", "/q"}:
            print("Bye!")
            break

        # File analysis command: /file path/to/file
        if cmd.startswith("/file "):
            path = cmd[len("/file ") :].strip()
            if not path:
                print("Usage: /file path/to/file")
                continue

            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                print(f"Error reading file '{path}': {e}")
                continue

            if not content.strip():
                print(f"File '{path}' is empty.")
                continue

            user_message = {
                "role": "user",
                "content": (
                    "Please analyze the following file. "
                    f"The file path is: {path}\n\n"
                    "```text\n" + content + "\n```"
                ),
            }
        else:
            user_message = {"role": "user", "content": user_input}

        messages.append(user_message)

        try:
            print("💭 Thinking...")

            full_response = ""
            for chunk in chat_stream(messages):
                if chunk:
                    safe_pretty_print(chunk)
                    full_response += chunk

            print()

            messages.append({"role": "assistant", "content": full_response})

        except KeyboardInterrupt:
            print("\n^C interrupted\n")
            if messages and messages[-1]["role"] == "user":
                messages.pop()
            continue
        except Exception as e:
            print(f"\nError: {e}\n")
            if messages and messages[-1]["role"] == "user":
                messages.pop()
            continue


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye!")
    except Exception as e:
        print(f"\nFatal error: {e}")
        sys.exit(1)
