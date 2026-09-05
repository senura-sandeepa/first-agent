from tools import calculator
from tools import multiply

def execute_tool (tool_name, arguments):

    if tool_name == "calculator":

        return calculator.calculator(
            arguments["a"],
            arguments["b"]
        )

    elif tool_name == "multiply":

        return multiply.multiply(
            arguments["a"],
            arguments["b"]
        )
    return None
