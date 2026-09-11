from tools.tool_registry import tool_functions

def execute_tool (tool_name, arguments):

    tool = tool_functions.get(tool_name)

    if tool is None:
        return None

    try:
        return tool(**arguments)
    except Exception as error:
        return f"Tool error: {error}"

