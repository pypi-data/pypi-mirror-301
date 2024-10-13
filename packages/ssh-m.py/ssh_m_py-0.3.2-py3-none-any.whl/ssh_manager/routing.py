from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText

from .shell import new_stored_entry, open_ssh
from .stored import append_to_stored, proceed_stored


def routing(is_new: bool) -> None:
    """Routing through script main functions
    If `-n` isn't specified checks storage, on empty case forces requires to make a new entry

    :param is_new: Launch arg
    :return: No.
    """
    if is_new:
        append_to_stored(new_stored_entry())
    elif not proceed_stored():
        print_formatted_text(FormattedText([("#abb2bf", "Storage is empty! Making an new connection\n")]))
        append_to_stored(new_stored_entry())
    open_ssh()
