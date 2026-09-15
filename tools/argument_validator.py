from tools.tool_registry import tools
from tools.tool_result import ToolResult

TYPE_MAPPING = {
    "number": (int, float),
    "string": (str,),
    "boolean": (bool,)
}

def validate_arguments(tool_name, arguments):

    tool = next(

        (

            tool for tool in tools
            if tool["function"]["name"] == tool_name

        ),
        None

    )

    parameters = tool["function"]["parameters"]

    required = parameters["required"]
    properties = parameters["properties"]

    # print(properties)
    # print(parameters["properties"].keys())
    # print(arguments)
    # print(required)
    # print(properties["a"]["type"])
    # print(properties.keys())

    #check for missing argument
    for argument in required:
        if argument not in arguments:

            return ToolResult(

                success = False,
                error = f"Missing required argument: {argument}",
                error_type = "invalid arguments"

            )

    #check for extra or unexpected argument
    for argument in arguments:
        if argument not in properties:

            return ToolResult(

                success = False,
                error = f"Unexpected argument: {argument}",
                error_type = "invalid arguments"

            )

    #check for validate argument type
    for argument in arguments:
        if argument in properties:
            expected_type = properties[argument]["type"]
            allowed_types = TYPE_MAPPING[expected_type]

            actual_value = arguments[argument]

            if not isinstance(actual_value, allowed_types):

                return ToolResult(

                    success = False,
                    error = f"Invalid type for argument: {argument}",
                    error_type = "invalid arguments"

                )

    # my code
    # for argument in arguments:
    #     if argument not in parameters["properties"].keys():
    #         print(f" Unexpected argument: {argument}")

    return ToolResult(success = True)
