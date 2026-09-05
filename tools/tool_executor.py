from tools import addition
from tools import multiply

def execute_tool (tool_name, arguments):

    if tool_name == "add":

        return addition.add(
            arguments["a"],
            arguments["b"]
        )

    elif tool_name == "multiply":

        return multiply.multiply(
            arguments["a"],
            arguments["b"]
        )
    return None
