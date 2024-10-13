import os.path
from json import load
from typing import List, Union

from pydantic import TypeAdapter

from .store_path import store_path
from ..connection import Connection, StoredConnection


def read_whole_store() -> List[StoredConnection]:
    """Get all stored entries as plain dicts

    :return: Storage object or [] if not exist
    """
    if os.path.exists(store_path):
        with open(store_path, 'r') as f:
            stored_connections = TypeAdapter(List[StoredConnection])
            loaded = stored_connections.validate_python(load(f))
        return loaded
    return []


def proceed_stored() -> Union[list, List[Connection]]:
    """Automatically read all stored entries and proceed it to `Connection` instances

    :return: List of all stored entries
    """
    stored = []
    loaded = read_whole_store()
    for i in loaded:
        stored.append(Connection(**i.dict()))

    return stored
