# First AI Agent

My first AI agent project built with Python and Ollama.

## Features

- Uses the Qwen3 4B model through Ollama
- Maintains conversation history
- Uses an `Agent` class to organize the AI logic
- Supports AI tool calling
- Includes multiple tools:
  - Addition
  - Multiplication
- Uses a tool registry to provide available tools to the AI
- Uses a tool executor to execute the tool requested by the AI
- Sends tool results back to the AI
- Automatically continues the tool-calling loop until the AI generates a final response

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
│   ├── addition.py
│   ├── multiply.py
│   ├── tool_executor.py
│   └── tool_registry.py
│
├── main.py
├── .gitignore
└── README.md
```

## How It Works

1. The user sends a message to the agent.
2. The agent sends the conversation and available tools to the Qwen model.
3. The model decides whether it needs to use a tool.
4. If a tool is requested, the tool executor runs the correct Python function.
5. The tool result is added to the conversation.
6. The agent sends the updated conversation back to the model.
7. This process continues until the model generates a final response.

## Example Flow

```text
User: What is 5 + 6?

        ↓

Qwen decides to call the "add" tool

        ↓

execute_tool("add", {"a": 5, "b": 6})

        ↓

addition.add(5, 6)

        ↓

Tool result: 11

        ↓

Result sent back to Qwen

        ↓

AI: The result of 5 + 6 is 11.
```

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

This project was created as part of my journey learning how AI agents, LLM tool calling, conversation memory, tool execution, and agent architecture work.
