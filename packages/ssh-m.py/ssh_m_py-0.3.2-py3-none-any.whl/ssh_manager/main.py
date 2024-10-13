from importlib.metadata import version
from json import JSONDecodeError
from os import environ

from pydantic_core import ValidationError

from .exception_handlers import handle_gracefully, format_exception
from .parse_args import parse_mode
from .routing import routing
from .runtime_exceptions import StorageProcessingError


def main():
    """Entrypoint for `setup.py`

    :return: No, lol.
    """
    print(f"ssh_manager "
          f"v{version('ssh_m.py') if not environ.get('SSH_M_PREVIEW_MODE') else '0.x.y'}:\n"
          )
    try:
        routing(parse_mode().n)
    except (StorageProcessingError,
            JSONDecodeError,
            ValidationError) as e:
        handle_gracefully(e)

    except KeyboardInterrupt:
        raise SystemExit(0)

    except Exception as e:
        raise format_exception(e)


if __name__ == "__main__":
    main()
