from pathlib import Path
from shutil import rmtree
from typing import Any
import json
from dataclasses import asdict, dataclass, Field, field
from datetime import datetime


@dataclass
class AppConfig:
    name: str = "PyLedger"
    version: str = "0.0.1"
    app_home: str = str(Path.home() / str(name + "-" + version))
    db_path: str = str(Path(app_home) / "App-DB")
    config_path: str = str(Path(app_home) / "config.json")
    log_path: str = str(Path(app_home) / "Logs")
    log_file: str = str(
        f"{Path(log_path)/ name}_{datetime.now().strftime('%x').replace('/','_')}.log"
    )

    paths: list[str] = field(
        default_factory=list,
    )

    def __post_init__(self):
        self.paths = [
            (self.app_home, "dir"),
            (self.db_path, "dir"),
            (self.config_path, "file"),
            (self.log_path, "dir"),
            (self.log_file, "file"),
        ]


@dataclass
class UserConfig:
    name: str
    password_hash: str
    db_path: str = str(Path(AppConfig().app_home) / "User-DB")
    config_path: str = str(Path(AppConfig().app_home) / ".user_config.json")

    paths: list[str] = field(
        default_factory=list,
    )

    def __post_init__(self):
        self.paths = [
            (self.db_path, "dir"),
            (self.config_path, "file"),
        ]


@dataclass
class AppDBConfig:
    api: str = "sqlite"
    name: str = AppConfig().name + "__" + AppConfig().version + ".db"
    db_path: Path = Path(
        str(Path(AppConfig().db_path) / str(datetime.now().year) / name)
    )
    echo: bool = False
    hide_parameters: bool = False


@dataclass
class UserDBConfig:
    api: str = "sqlite"
    name: str = ""
    db_path: Path = Path(
        str(Path(AppConfig().db_path) / str(datetime.now().year) / str(name + ".db"))
    )
    echo: bool = False

    hide_parameters: bool = False


class Json:
    def __init__(self, fp: Path | str) -> None:
        self.fp = Path(fp)

    def write_(self, content: dict[str, Any] | str) -> None:
        if not self.fp.parent.exists():
            self.fp.parent.mkdir(parents=True, exist_ok=True)
        with open(self.fp, "w+") as file:
            if not isinstance(content, str) and isinstance(content, dict):
                content = json.dumps(content, indent=4)
            file.write(content)

    def read_(self) -> dict[str, Any] | None:
        if self.fp.exists():
            with open(self.fp, "r+") as file:
                return json.loads(file.read())
        else:
            return None


class ConfigHandler:
    def __init__(self, conf: AppConfig | UserConfig | None = None) -> None:
        self.config = conf
        self.file = Json(self.config.config_path)

    def write(self, content: str | dict[str, Any]):
        try:
            self.file.write_(content=content)
            return True
        except IOError as e:
            print(f"{e}")
            return False

    def read(self) -> dict[str, Any] | None:
        return self.file.read_()


def create_config(conf: AppConfig | UserConfig | None = None):
    if not Path(conf.config_path).exists():
        ConfigHandler(conf).write(asdict(conf))


def update_config(conf: AppConfig | UserConfig | None = None):
    if Path(conf.config_path).exists():
        ConfigHandler(conf).write(asdict(conf))


def get_config(conf: AppConfig | UserConfig | None = None):
    if Path(conf.config_path).exists():
        return ConfigHandler(conf).read()


def create_app_dirs(
    conf: AppConfig | UserConfig | None = None, force_recreate: bool = False
):
    def create_file(path: Path, exists_ok: bool = False):
        path.touch(exist_ok=exists_ok)

    def create_dir(path: Path, parents: bool = True, exists_already: bool = False):
        path.mkdir(parents=parents, exist_ok=exists_already)

    def delete_file(path: Path):
        path.unlink()

    def delete_dir(path: Path):
        path.rmdir()

    def delete_tree(path: Path):
        rmtree(path)

    paths = [(Path(p[0]), p[1]) for p in conf.paths]

    for path, type in paths:
        if not force_recreate:
            if type == "file":
                try:
                    create_file(path, exists_ok=True)
                except Exception:
                    create_dir(path.parent, exists_already=True)
            if type == "dir" or "folder":
                create_dir(path)
        else:
            if type == "file":
                try:
                    create_file(path)
                except Exception:
                    create_dir(path.parent)
            if type == "dir" or "folder":
                create_dir(path)
