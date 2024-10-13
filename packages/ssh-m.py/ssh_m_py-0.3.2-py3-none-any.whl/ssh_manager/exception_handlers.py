from json import JSONDecodeError

from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from pydantic_core import ValidationError

from .runtime_exceptions import StorageProcessingError


def handle_gracefully(e):
    formatted_text = []
    hide_post: bool = False

    if isinstance(e, StorageProcessingError):
        formatted_text = [("", e.ctx or "")]
        if type(e.accent) is str:
            formatted_text += [("", "\n"), ("#ff0000 underline", e.accent)]
        hide_post = e.hide_post
    elif isinstance(e, JSONDecodeError):
        formatted_text = [("", f"JSON decoding error at line {e.lineno} col {e.colno}"),
                          ("", "\n"), ("#ff0000 underline", e.msg)]
    elif isinstance(e, ValidationError):
        formatted_text = [("", f"Pydantic validate failed with:\n")]
        for _ in e.errors():
            formatted_text += [("", "    "), ("#ff0000 underline", f"{_.get('msg')}{_.get('loc')}")]
            formatted_text += [("#abb2bf", f" at {_.get('input')}\n")]

    if not hide_post:
        formatted_text += [("", "\n\n"), ("#abb2bf", "Most likely this was caused by fact that you edited the storage")]
    print_formatted_text(FormattedText(formatted_text))
    raise SystemExit(1)


def format_exception(e) -> type[Exception]:
    return e
