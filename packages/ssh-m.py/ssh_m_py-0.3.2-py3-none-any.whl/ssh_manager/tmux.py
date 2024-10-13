import os

from .connection import Connection
from .parse_args import parse_mode_env, ActionMode


def run_in_tmux(connection: Connection) -> None:
    """Run SSH connection with specified TMUX features
    Could rename an active window to user@hostname and terminates window on connection close

    :param connection: `Connection` to be used in SSH session
    """
    if not parse_mode_env(ActionMode.NO_RENAME):
        os.system(f"tmux rename-window '{connection}'")
    os.system(connection.connect_prompt())
    if not parse_mode_env(ActionMode.NO_CLOSE):
        os.system("kill -9 %d" % (os.getppid()))  # Dirty hack from Foo Bah to close tty after ssh ends
    if not parse_mode_env(ActionMode.NO_RENAME):
        os.system("tmux set automatic-rename on")
