# First AI Agent

My first AI agent project built with Python and Ollama.

## Features

- Uses the Qwen3 4B model through Ollama
- Maintains conversation history
- Uses an `Agent` class to organize the AI logic
- Supports AI tool calling
- Includes a calculator tool for addition
- Sends tool results back to the AI so it can generate a final response

## Project Structure

```text
first-agent/
│
├── agent/
│   ├── __init__.py
│   └── agent.py
│
├── tools/
│   ├── __init__.py
│   └── calculator.py
│
├── main.py
├── .gitignore
└── README.md
```

## How It Works

1. The user sends a message to the agent.
2. The agent sends the conversation to the Qwen model.
3. If the model requests a tool, the Python application executes that tool.
4. The tool result is added to the conversation.
5. The model receives the result and generates a final response.

## Requirements

- Python
- Ollama
- Qwen3 4B model

Install the Python dependency:

```bash
pip install ollama
```

Make sure Ollama is running and the model is available:

```bash
ollama pull qwen3:4b
```

## Run

```bash
python main.py
```

Type `exit` to close the application.

## Learning Project

This project was created as part of my journey learning how AI agents, LLM tool calling, conversation memory, and agent architecture work.
