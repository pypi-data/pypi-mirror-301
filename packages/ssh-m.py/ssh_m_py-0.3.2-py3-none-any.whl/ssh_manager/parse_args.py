import argparse
import os
from enum import Enum


class ActionMode(Enum):
    """Available modes in TMUX environment

    """
    NO_CLOSE = 1
    NO_RENAME = 2


def parse_mode_env(action: ActionMode) -> bool:
    """Parse envvars and launch arguments to determine correct mode

    :param action: Requested tmux mode to be checked

    :return: Mode status
    """
    match action:
        case ActionMode.NO_CLOSE:
            return bool(parse_mode().C or os.environ.get("SSH_M_C") or os.environ.get("SSH_M_PREVIEW_MODE"))
        case ActionMode.NO_RENAME:
            return bool(parse_mode().R or os.environ.get("SSH_M_R"))
    return False


def parse_mode() -> argparse.Namespace:
    """Parse launch arguments
    Should be called before routing and pass arguments to it

    :return: Parsed arguments `Namespace`
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-n',
        default=False,
        action='store_true',
        help=(
            'Proceed new SSH connection to storage\n'
            'Executed by default if storage is empty.'
        )
    )
    parser.add_argument(
        '-R',
        default=False,
        action='store_true',
        help=(
            'Acts same as $SSH_M_R\n'
            'Prevents renaming TMUX window on SSH connection.'
        )
    )
    parser.add_argument(
        '-C',
        default=False,
        action='store_true',
        help=(
            'Acts same as $SSH_M_C\n'
            'Prevents closing of TMUX after SSH is disconnected.'
        )
    )
    return parser.parse_args()
