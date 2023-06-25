import pathlib
from rich.console import Console


def get_console(record: bool = False, file: pathlib.Path | None = None):
    """Returns a rich console.
    By Default:
    theme: NIGHT_THEME
    record: False
    """
    return Console(record=record, file=file)
