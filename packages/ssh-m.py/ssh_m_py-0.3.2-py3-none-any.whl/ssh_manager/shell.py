import os
from enum import Enum
from pathlib import Path
from typing import Optional, Tuple, Dict

from InquirerPy import inquirer, get_style
from InquirerPy.base.control import Choice
from InquirerPy.enum import INQUIRERPY_POINTER_SEQUENCE as POINTER_CODE
from InquirerPy.validator import PathValidator

from .connection import Connection
from .runtime_exceptions import RuntimeProcessingError, StorageProcessingError
from .stored import proceed_stored, append_to_stored, remove_from_stored
from .tmux import run_in_tmux


def one_time_selection() -> Optional[Connection]:
    """Start an interactive selection

    :return: Selected connection instance
    """

    class _MenuAction(Enum):
        """Enum representation os selected action in menu
        """
        Select = 0
        New = 1
        Delete = 2

    store = proceed_stored()
    menu = inquirer.select(
        message="Select SSH user:",
        qmark="",
        amark=POINTER_CODE,
        vi_mode=True,
        show_cursor=False,
        long_instruction="new: n, delete: d\nexit: C-c, q",
        keybindings={"interrupt": [{"key": "q"}, {"key": "c-c"}]},
        choices=[Choice(value=(_MenuAction.Select, i), name=str(_)) for i, _ in enumerate(store)],
        style=get_style({"answermark": "#61afef"}, style_override=False)
    )

    @menu.register_kb("d")
    def _delete_entry(ctx):
        """Process "d" button as Delete action
        """
        ctx.app.exit(result=(_MenuAction.Delete, menu.result_value[1]))

    @menu.register_kb('n')
    def _new_entry(ctx):
        """Process "n" button as New action
        """
        ctx.app.exit(result=(_MenuAction.New, -1))

    selected: Tuple[_MenuAction, int] = menu.execute()
    match selected[0]:
        case _MenuAction.New:
            append_to_stored(new_stored_entry())
            return None
        case _MenuAction.Delete:
            if inquirer.confirm(message=f"Delete {store[selected[1]]}?").execute():
                remove_from_stored(selected[1])
                if len(store) == 1:
                    raise StorageProcessingError(message="No more records left after",
                                                 accent=f"{store[selected[1]]}",
                                                 not_user_fault=True)
            return None
        case _MenuAction.Select:
            return store[selected[1]]


def new_stored_entry() -> Connection:
    """Step-by-step creating new stored info

    :return: Recently created connection instance
    """

    class _ConnectionType(str, Enum):
        Environment = "Environment variable"
        Key = "SSH key"

    def _inquirer_wrapper_input(message: str, **kwargs) -> str:
        """Pre-configured :inquirer.text with provided placeholder
        Additional arguments would be passed as kwargs

        :return: Answer to text input
        """
        return inquirer.text(
            message=message,
            amark=POINTER_CODE,
            validate=lambda _: len(_) > 0,
            long_instruction="exit: C-c",
            **kwargs
        ).execute()

    def _auth_method() -> Dict[str, str]:
        # TODO: Refactor repeating code
        select_auth_method = inquirer.select(
            message="Select connection type",
            vi_mode=True,
            show_cursor=False,
            long_instruction="exit: C-c",
            transformer=lambda _: "Env" if _ == _ConnectionType.Environment else "Key",
            choices=[Choice(_, _.value) for _ in _ConnectionType]
        ).execute()
        match select_auth_method:
            case _ConnectionType.Environment:
                return {"named_passwd": _inquirer_wrapper_input(
                    "Environment variable prefix",
                    instruction="(eg. server in server_user):"
                )}
            case _ConnectionType.Key:
                key_file_relative = inquirer.filepath(
                    message="Enter path to key file",
                    validate=PathValidator(is_file=True, message="Input is not a file"),
                    only_files=True,
                    long_instruction="exit: C-c"
                ).execute()
                return {"key_file": str(Path(key_file_relative).resolve())}
            case _:
                raise RuntimeProcessingError("Selection error for new connection",
                                             f"Chosen method was: {select_auth_method}")

    return Connection(
        hostname=_inquirer_wrapper_input("Hostname", instruction="(eg. google.com):"),
        remote_user=_inquirer_wrapper_input("Remote user:"),
        **_auth_method()
    )


def open_ssh() -> None:
    """Start an SSH connection
    Checks whenever runs inside TMUX session, then proceeds further handling in `run_in_tmux`

    :return: No.
    """
    connection = one_time_selection()
    if not connection:
        return open_ssh()

    if os.environ.get("TMUX"):
        run_in_tmux(connection)
    else:
        os.system(connection.connect_prompt())
