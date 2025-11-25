# CLI_Agent

A lightweight CLI AI assistant built on top of a large language model. Supports both interactive conversations and one-shot analysis via pipes.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

- 🤖 **Interactive chat** – natural language interaction with an AI assistant
- 🔄 **Pipe support** – accept input from stdin and exit after one response
- 📤 **Clean output** – streaming output with no extra blank lines
- ⚡ **Streaming responses** – tokens are printed in real time
- 🔐 **Safe configuration** – API key is read from environment variables only
  

## 🚀 Quick Start

### Requirements

- Python 3.10+
- An API key for the QNAI-compatible chat completion API

### Installation

1. **Clone the project**

```bash
git clone https://github.com/Bernardyao/CLI_Agent.git
cd CLI_Agent
```

2. **Create a virtual environment (recommended)**

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate   # Windows
```

3. **Configure API key**

```bash
export QNAI_API_KEY="your_api_key_here"  # Linux/macOS
# or on Windows PowerShell
$Env:QNAI_API_KEY="your_api_key_here"
```

> The current implementation only reads the key from environment variables. Do **not** commit your key into `config.py` or any other file.

4. **Install dependencies**

```bash
pip install -r requirements.txt
```

### Usage

#### Interactive mode

```bash
python agent.py
```

Type your question after the `ag>` prompt. To exit, use one of:

- `/exit`
- `/quit`
- `/q`
- `Ctrl+C` or `Ctrl+D` (EOF)

#### Analyze a file in interactive mode

Use the `/file` command followed by a path:

```bash
python agent.py
ag> /file path/to/file.py
```

The agent will read the file content and ask the model to analyze it using the current conversation context.

#### Pipe mode (one-shot analysis)

```bash
echo "Explain this code" | python agent.py
cat file.txt | python agent.py
```

In pipe mode, the agent reads all stdin, prints a single streaming answer, then exits automatically.

## 📁 Project Structure

```text
CLI_Agent/
├── agent.py              # Main entry point
├── config.py             # API configuration
├── modules/              # Core modules
│   ├── input_handler.py  # Input and pipe handling
│   ├── llm_client.py     # LLM client (streaming + non-streaming)
│   └── utils.py          # Output helpers
├── .gitignore            # Git ignore rules
├── LICENSE               # MIT license
└── README.md             # Project documentation
```

## 🛠️ Core Behavior

### 1. Input handling

- Detects piped input from stdin (non-TTY)
- Uses standard `input()` for interactive terminals
- Supports explicit exit commands in interactive mode

### 2. Streaming responses

- Uses the chat completion API with `stream=true`
- Prints tokens as they arrive using `safe_pretty_print`

### 3. Configuration

- API key is read from `QNAI_API_KEY`
- Base URL and model are defined in `config.py`

Example `config.py` excerpt:

```python
import os

API_KEY = os.getenv("QNAI_API_KEY")
BASE_URL = "https://api.qnaigc.com/v1/chat/completions"
MODEL = "deepseek/deepseek-v3.1-terminus"
```

## 🔧 Development

### Quick checks

```bash
# Basic output test
python -c "from modules.utils import pretty_print; pretty_print('Hello, World!')"

# Pipe behavior test
echo "test" | python agent.py
```

## 📝 Changelog (excerpt)

- **v2.0.0 (2025-11-25)**
    - Fixed blank output issues
    - Simplified code structure and improved robustness
    - Refined pipe handling and exit behavior
    - Added a more complete `.gitignore`

## 📄 License

This project is licensed under the MIT License – see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgements

- DeepSeek for the underlying model
- The Python ecosystem for libraries and tooling

