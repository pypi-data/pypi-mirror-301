from typing import Any, Optional, Union


class RuntimeProcessingError(Exception):
    """Exception should be raised when normally impossible things are happen
    Receives multiple arguments to be shown, each starting with newline
    Normally should be never occurred during usage

    Ends with link to GitHub Issues
    """

    def __init__(self, ctx: str, *args_ctx: Any):
        self.ctx = ctx
        for aux_ctx in args_ctx:
            self.ctx += f"\n{aux_ctx}"
        self.ctx += ("\n\nThis error should be normally never occurred.\n"
                     "Please open a new ticket on Github Issues with steps to reproduce and trace above\n"
                     "https://github.com/LoliPain/ssh_manager/issues/new?assignees=&labels=invalid&projects=&template"
                     "=report-an-invalid-or-unexpected-behavior.md&title=")
        super().__init__(self.ctx)


class StorageProcessingError(Exception):
    """Raised in cases when seemingly user modified storage between script usage
    Highlights the part that occurred problem as additional context in :accent arg

    :accent List of prompt_toolkit colored tuples or plain str to be colored red
    """

    def __init__(
            self,
            message: Optional[str] = None,
            accent: Optional[Union[tuple[str, str], str]] = None,
            not_user_fault: bool = False,
    ):
        self.ctx = message
        self.accent = accent
        self.hide_post = not_user_fault
        super().__init__(self.ctx or self.accent)
