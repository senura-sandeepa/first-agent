from tools import addition
from tools import multiply

tool_modules = [
    addition,
    multiply
]

tools = []

tool_functions = {}

for module in tool_modules:

    tools.extend(module.tool_definition)
    tool_name = module.tool_definition[0]["function"]["name"]
    tool_functions[tool_name] = getattr(module, tool_name)
