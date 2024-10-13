from json import dumps

from pydantic_core import to_jsonable_python

from .read import read_whole_store
from .store_path import store_path
from ..connection import Connection


def append_to_stored(connection: Connection) -> None:
    """Add new connection to storage
    If storage file not exists creates it

    :param connection: Freshly created connection
    :return: No.
    """
    loaded = read_whole_store()
    with open(store_path, 'w+') as f:
        loaded.append(connection.to_model())
        f.write(dumps(to_jsonable_python(loaded, exclude_none=True), indent=2))
    return None


def remove_from_stored(stored_index: int) -> None:
    """Removes existing stored connection by given index

    :param stored_index: Index of record to be removed
    :return: No.
    """
    loaded = read_whole_store()
    with open(store_path, 'w+') as f:
        loaded.pop(stored_index)
        f.write(dumps(to_jsonable_python(loaded, exclude_none=True), indent=2))
    return None
