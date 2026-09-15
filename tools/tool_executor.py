from tools.tool_registry import tool_functions
from tools.tool_result import ToolResult
from tools.argument_validator import validate_arguments

def execute_tool (tool_name, arguments):

    tool = tool_functions.get(tool_name)

    if tool is None:

        # 3. Tool doesn't exist
        return ToolResult(
            success = False,
            error = f"Unknown tool: {tool_name}",
            error_type = "unknown tool"
        )

    try:

        validation = validate_arguments(tool_name, arguments)

        if not validation.success:
            return validation

        # 1. Tool succeeds
        result = tool(**arguments)

        # print("DEBUG ARGUMENTS:", arguments)

        return ToolResult(
            success = True,
            result = result
        )

    except Exception as error:

        # 2. Tool throws an exception
        return ToolResult(
            success = False,
            error = str(error),
            error_type = "execution error"
        )