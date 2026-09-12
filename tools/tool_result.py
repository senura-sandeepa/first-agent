class ToolResult:

    def __init__(
            self,
            success: bool,
            result=None,
            error: str | None = None,
            error_type: str | None = None
    ):

        self.success = success
        self.result = result
        self.error = error
        self.error_type = error_type

    def __str__(self) -> str:

        if self.success:
            return str(self.result)

        return f"Tool error: {self.error}"