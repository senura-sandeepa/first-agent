# First AI Agent

My first AI agent project built with Python and Ollama.

This project is a learning-focused implementation of an AI agent from scratch, with an emphasis on understanding agent architecture, LLM tool calling, deterministic tool execution, conversation history, and error handling.

## Features

- Uses the Qwen3 4B model through Ollama
- Maintains conversation history
- Uses an `Agent` class to organize the AI logic
- Supports AI tool calling
- Includes multiple tools:
  - Addition
  - Multiplication
- Uses a tool registry to provide available tools to the AI
- Dynamically maps registered tool names to Python functions
- Uses a tool executor to execute tools requested by the AI
- Uses a structured `ToolResult` object for tool execution results
- Tracks tool execution errors with an `error_type`
- Validates tool arguments before execution
- Checks for missing required arguments, unexpected arguments, and invalid argument types
- Uses a type mapping for supported tool schema types
- Currently distinguishes between:
  - `unknown tool`
  - `invalid arguments`
  - `execution error`
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
│   ├── tool_registry.py
│   ├── tool_result.py
│   └── argument_validator.py
│
├── main.py
├── .gitignore
└── README.md
```

## Architecture

The current architecture separates the responsibilities of the agent, tool registry, tool execution, and tool results.

```text
                    ┌───────────────┐
                    │    main.py    │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │     Agent     │
                    │               │
                    │ - messages    │
                    │ - model       │
                    │ - tools       │
                    │ + chat()      │
                    └───────┬───────┘
                            │
                    calls / uses
                            │
             ┌──────────────┴──────────────┐
             ▼                             ▼
    ┌─────────────────┐          ┌─────────────────┐
    │ Tool Registry   │          │ Tool Executor   │
    │                 │          │                 │
    │ - tool_modules  │          │ execute_tool()  │
    │ - tools         │          │                 │
    │ - tool_functions│          └────────┬────────┘
    └───────┬─────────┘                   │
            │                             │
       registers                    returns
            │                             ▼
      ┌─────┴─────┐              ┌─────────────────┐
      ▼           ▼              │   ToolResult    │
 ┌─────────┐ ┌──────────┐        │                 │
 │ addition│ │ multiply │        │ - success       │
 │ add()   │ │multiply()│        │ - result        │
 └─────────┘ └──────────┘        │ - error         │
                                 │ - error_type    │
                                 │ + __str__()      │
                                 └─────────────────┘
```

`addition.py` and `multiply.py` are tool modules/functions rather than classes. `ToolResult` is currently the main class used to represent the outcome of tool execution. `argument_validator.py` is responsible for validating arguments before an existing tool is executed.

## How It Works

1. The user sends a message to the agent.
2. `Agent.chat()` adds the user message to the conversation history.
3. The agent sends the conversation and available tools to the Qwen model.
4. The model decides whether it needs to use a tool.
5. If a tool is requested, the agent passes the tool name and arguments to `execute_tool()`.
6. The tool executor looks up the requested function through the tool registry.
7. The executor validates the supplied arguments using `validate_arguments()`.
8. If validation fails, the validation `ToolResult` is returned and the tool is not executed.
9. If validation succeeds, the requested Python function is executed.
10. The executor returns a `ToolResult` object describing the outcome.
11. If execution succeeds, the result is added to the conversation as a tool message.
12. The updated conversation is sent back to Qwen.
13. The tool-calling loop continues until Qwen produces a final response.
14. If a tool fails, the agent currently handles the failure according to its `error_type`.

## Tool Registry

The tool registry keeps the available tools in one place.

Each tool module provides:

- A Python function
- A `tool_definition` describing the function to the LLM

The registry collects the definitions and dynamically maps the tool name to the actual Python function.

For example:

```python
tool_name = module.tool_definition[0]["function"]["name"]
tool_functions[tool_name] = getattr(module, tool_name)
```

This means a tool does not need to be manually added to a separate function mapping.

## Argument Validation

Before a tool is executed, `argument_validator.py` checks the arguments against the tool's `tool_definition`.

The validator currently checks:

```text
Required arguments
        ↓
Unexpected arguments
        ↓
Argument types
        ↓
ToolResult(success=True)
```

For invalid input, it returns a failed `ToolResult`:

```python
ToolResult(
    success=False,
    error="Invalid type for argument: a",
    error_type="invalid arguments"
)
```

Supported schema types are currently mapped as:

```python
TYPE_MAPPING = {
    "number": (int, float),
    "string": (str,),
    "boolean": (bool,)
}
```

This validation layer prevents invalid arguments from reaching the actual Python tool function.

## Tool Execution

The tool executor is responsible for safely locating and executing a requested tool.

```text
Tool name + arguments
        ↓
tool_registry.tool_functions
        ↓
Python function
        ↓
ToolResult
```

The executor currently handles three failure categories:

```text
unknown tool
invalid arguments
execution error
```

This separation is the beginning of a more robust error-handling system.

## ToolResult

`ToolResult` provides a consistent structure for tool execution outcomes.

```python
ToolResult(
    success=True,
    result=12
)
```

or, when a tool fails:

```python
ToolResult(
    success=False,
    error="division by zero",
    error_type="execution error"
)
```

The class contains:

- `success` — whether the tool executed successfully
- `result` — the successful tool result
- `error` — the error message when execution fails
- `error_type` — the category of failure

It also implements `__str__()` so the object can be converted into a human-readable string when sending the result back to the model.

## Example Flow

```text
User: What is 5 + 6?

        ↓

Agent sends the request and available tools to Qwen

        ↓

Qwen decides to call the "add" tool

        ↓

execute_tool("add", {"a": 5, "b": 6})

        ↓

tool registry finds addition.add()

        ↓

Argument validation

        ↓

Arguments valid ✅

        ↓

addition.add(5, 6)

        ↓

ToolResult(success=True, result=11)

        ↓

Result sent back to Qwen

        ↓

AI: The result of 5 + 6 is 11.
```

## Error Handling Example

If a tool throws an exception:

```text
addition.add()
        ↓
Exception
        ↓
ToolResult(
    success=False,
    error="division by zero",
    error_type="execution error"
)
        ↓
Agent
        ↓
Tool failed: division by zero
```

If the requested tool does not exist:

```text
Requested tool
        ↓
Tool Registry
        ↓
Tool not found
        ↓
ToolResult(
    success=False,
    error_type="unknown tool"
)
        ↓
Agent
        ↓
"I don't know how to use the tool..."
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

This project was created as part of my journey learning how AI agents, LLM tool calling, conversation memory, tool execution, error handling, and agent architecture work.

The goal is not only to make an agent that works, but to understand and gradually build its architecture from the ground up.

## Current Development Direction

The project is being developed incrementally.

Current focus:

- Building a reliable argument validation layer
- Keeping tool execution responsibilities separated
- Improving tool error categorization
- Building a more reliable recovery and retry system

Future improvements will be added as the architecture evolves.
