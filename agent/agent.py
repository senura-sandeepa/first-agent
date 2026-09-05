from ollama import chat

from tools import tool_registry
from tools.tool_executor import execute_tool

class Agent:

    def __init__(self):

        #system message that saying always start response in English language
        self.messages = [{

            "role": "system",
            "content": "You are a helpful AI assistant. Always respond in English. "
                       "start with just saying HI! i mean just for welcome message, then respond naturally"

        }]

        #model name
        self.model = "qwen3:4b"

        self.tools = tool_registry.tools

    def chat (self, user_input):

        self.messages.append({

            "role": "user",
            "content": user_input

        })

        while True:

            response = chat (

                model = self.model,
                messages = self.messages,
                tools = self.tools

            )

            self.messages.append(response.message)

            # print("DEBUG RESPONSE:", response.message)
            # print("DEBUG TOOL CALLS:", response.message.tool_calls)

            if not response.message.tool_calls:

                # print("DEBUG CONTENT:", repr(response.message.content))
                # print("DEBUG THINKING:", repr(response.message.thinking))
                # print("DEBUG TOOL CALLS:", response.message.tool_calls)

                return  response.message.content

            for tool_call in response.message.tool_calls:

                result = execute_tool(

                    tool_call.function.name,
                    tool_call.function.arguments

                )

                self.messages.append({
                    "role": "tool",
                    "tool_name": tool_call.function.name,
                    "content": str(result)
                })

