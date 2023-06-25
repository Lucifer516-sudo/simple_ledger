"""Just has some basic file operations that are modified for the use of my application"""

import shutil
import pathlib
from typing import Any, Literal
import json
import toml


def write(
    content: str | dict,
    to_file: pathlib.Path,
    file_extension: Literal["json", "txt", "toml"] | None = None,
    force_create: bool = False,
):
    if file_extension is "json" and isinstance(content, dict):
        content = json.dumps(content, indent=2)

    elif file_extension is "toml" and isinstance(content, dict):
        content = toml.dumps(content)

    elif file_extension is "txt" or None:
        content = str(content)
    else:
        pass  # Not gd to silence

    if force_create:
        if to_file.exists() and to_file.is_file():
            to_file.unlink()
            to_file.touch()
            with open(to_file, "a+") as file:
                file.write(content)
                return True
        else:
            return False
    elif not force_create:
        if not to_file.exists():
            to_file.touch()
            with open(to_file, "a+") as file:
                file.write(content)
                return True
        else:
            return False
    else:
        ...  # not gd practice


def read(
    from_file: pathlib.Path,
    file_extension: Literal["json", "txt", "toml"] | None = None,
) -> dict[str, Any] | str | None:
    if from_file.exists():
        if file_extension is "json":
            return json.load(from_file)
        if file_extension is "toml":
            return toml.load(from_file)
        if file_extension is ("txt" or None):
            with open(from_file) as file:
                return file.read()
    else:
        # raise an error
        return


def create_folder(
    path: pathlib.Path, force: bool = True, parents: bool = False
) -> bool | None:
    if force:
        if path.exists():
            if remove_folder_recursively(path):  # deletes the contents too...
                path.mkdir(parents=parents)
                return True
            else:
                return False
    elif not force:
        if not path.exists():
            path.mkdir(parents=parents)
            return True
        else:
            return False
    else:
        # Raise value error
        return


def remove_folder_recursively(path: pathlib.Path) -> bool:
    try:
        shutil.rmtree(path)
        return True
    except Exception:
        # not interested in raising error
        return False
