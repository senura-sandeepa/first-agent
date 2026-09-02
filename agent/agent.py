from ollama import chat

from tools import calculator as calc

class Agent:

    def __init__(self):

        #system message that saying always start response in English language
        self.messages = [{

            "role": "system",
            "content": "You are a helpful AI assistant. Always respond in English."

        }]

        #model name
        self.model = "qwen3:4b"

        self.tools = calc.calculator_tool

    def chat (self, user_input):

        self.messages.append({

            "role": "user",
            "content": user_input

        })

        response = chat (

            model = self.model,
            messages = self.messages,
            tools = self.tools

        )

        self.messages.append(response.message)

        if response.message.tool_calls:
            tool_call = response.message.tool_calls[0]

            if tool_call.function.name == "calculator":
                a = tool_call.function.arguments["a"]
                b = tool_call.function.arguments["b"]

                result = calc.calculator(a, b)

                # print("Tool result", result)

                self.messages.append({
                    "role": "tool",
                    "content": str(result)
                })

                final_response = chat(
                    model = self.model,
                    messages = self.messages,
                    tools = self.tools
                )

                return final_response.message.content
            return None

        return response.message.content