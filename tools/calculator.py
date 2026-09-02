def calculator (a, b):
    return a + b

calculator_tool = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Add two numbers together",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "The first number"
                    },
                    "b": {
                        "type": "number",
                        "description": "The second number"
                    }
                },
                "required": ["a", "b"]
            }
        }
    }
]
