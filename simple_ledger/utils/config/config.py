from datetime import date, datetime
from pathlib import Path
from typing import Any, Literal
from simple_ledger.utils.config._config import (
    UserConfig,
    UserInfo,
    UserDBConfig,
    AppInfo,
    AppDBConfig,
    AppConfig,
    LoggingConfig,
)
import logging
from simple_ledger.utils.file_handling.file_ops import (
    write,
    read,
    remove_folder_recursively,
)
from simple_ledger.utils.timer import timer
from simple_ledger.utils.rich_printing._get_console import get_console

console = get_console()

ALL_CONFIGS: dict = {
    "UserConfig": UserConfig,
    "UserInfo": UserInfo,
    "UserDBConfig": UserDBConfig,
    "AppInfo": AppInfo,
    "AppDBConfig": AppDBConfig,
    "AppConfig": AppConfig,
    "LoggingConfig": LoggingConfig,
}


def generate_app_config(
    console=console,
    *,
    DEFAULT_NAME: str | None = None,
    DEFAULT_VERSION: tuple[int, ...] | None = None,
    DEFAULT_RELEASE: str | None = None,
    DEFAULT_APP_HOME_PATH: Path | None = None,
    DEFAULT_APP_DB_DIR: Path | None = None,
    DEFAULT_APP_LOG_DIR: Path | None = None,
    DEFAULT_APP_CONFIG_PATH: Path | None = None,
    DEFAULT_DB_API: str | None = None,
    DEFAULT_DB_FILE_NAME: str | None = None,
    DEFAULT_DB_DIR_PATH: Path | None = None,
    DEFAULT_DB_ECH0: bool | None = None,
    DEFAULT_DB_HIDE_PARAMETERS: bool | None = None,
    DEFAULT_LOGGING_LEVEL: int | str | None = None,
    DEFAULT_LOG_FILE_NAME: str | None = None,
    DEFAULT_LOG_OUTPUT_DIR: Path | None = None,
    DEFAULT_RENDER_TO_SCREEN: bool | None = None,
) -> AppConfig:  # type: ignore
    """Generated Default App Config"""
    if (
        DEFAULT_NAME is None
        and DEFAULT_VERSION is None
        and DEFAULT_RELEASE is None
        and DEFAULT_APP_HOME_PATH is None
        and DEFAULT_APP_DB_DIR is None
        and DEFAULT_APP_LOG_DIR is None
        and DEFAULT_APP_CONFIG_PATH is None
        and DEFAULT_DB_API is None
        and DEFAULT_DB_FILE_NAME is None
        and DEFAULT_DB_DIR_PATH is None
        and DEFAULT_DB_ECH0 is None
        and DEFAULT_DB_HIDE_PARAMETERS is None
        and DEFAULT_LOGGING_LEVEL is None
        and DEFAULT_LOG_FILE_NAME is None
        and DEFAULT_LOG_OUTPUT_DIR is None
        and DEFAULT_RENDER_TO_SCREEN is None
    ):
        DEFAULT_NAME = "PyLedger"
        DEFAULT_VERSION = (0, 0, 6)
        DEFAULT_RELEASE = "dev"
        DEFAULT_APP_HOME_PATH = (
            Path.home()
            / f"{DEFAULT_NAME}-{'.'.join([str(_) for _ in DEFAULT_VERSION])}@{DEFAULT_RELEASE}"
        )
        DEFAULT_APP_DB_DIR = (
            DEFAULT_APP_HOME_PATH / "DataBases" / f"{str(datetime.today().year)}"
        )
        DEFAULT_APP_LOG_DIR = (
            DEFAULT_APP_HOME_PATH / "Logs" / f"{str(datetime.today().year)}"
        )
        DEFAULT_APP_CONFIG_PATH = (
            DEFAULT_APP_HOME_PATH
            / f"{DEFAULT_NAME}-{'.'.join([str(_) for _ in DEFAULT_VERSION])}@{DEFAULT_RELEASE}_config.toml"
        )
        DEFAULT_DB_API = "sqlite"
        DEFAULT_DB_FILE_NAME = DEFAULT_NAME + ".db"
        DEFAULT_DB_DIR_PATH = DEFAULT_APP_DB_DIR / f"{DEFAULT_NAME}-DBs"
        DEFAULT_DB_ECH0 = False
        if DEFAULT_RELEASE == "dev":
            DEFAULT_DB_HIDE_PARAMETERS = False
            DEFAULT_LOGGING_LEVEL = logging.DEBUG
            DEFAULT_RENDER_TO_SCREEN = True
        else:
            DEFAULT_DB_HIDE_PARAMETERS = False
            DEFAULT_LOGGING_LEVEL = logging.DEBUG
            DEFAULT_RENDER_TO_SCREEN = False
        _that_day: datetime = datetime.now()
        DEFAULT_LOG_FILE_NAME = f"{DEFAULT_NAME}_{'.'.join([str(_) for _ in DEFAULT_VERSION])}>>{DEFAULT_RELEASE.upper()}__{_that_day.strftime('%d_%m_%Y::%H_%M_%S::%p')}.log"
        DEFAULT_LOG_OUTPUT_DIR = (
            DEFAULT_APP_LOG_DIR / f"{DEFAULT_NAME}-Logs" / _that_day.strftime("%B")
        )

        _conf = AppConfig(  # type: ignore
            NAME=DEFAULT_NAME,
            VERSION=DEFAULT_VERSION,
            RELEASE=DEFAULT_RELEASE,
            APP_HOME_PATH=DEFAULT_APP_HOME_PATH,
            APP_DB_DIR=DEFAULT_APP_DB_DIR,
            APP_LOG_DIR=DEFAULT_APP_LOG_DIR,
            CONFIG_PATH=DEFAULT_APP_CONFIG_PATH,
            DB_API=DEFAULT_DB_API,
            DB_FILE_NAME=DEFAULT_DB_FILE_NAME,
            DB_DIR_PATH=DEFAULT_DB_DIR_PATH,  # type: ignore
            DB_ECH0=DEFAULT_DB_ECH0,
            DB_HIDE_PARAMETERS=DEFAULT_DB_HIDE_PARAMETERS,
            LOGGING_LEVEL=DEFAULT_LOGGING_LEVEL,
            LOG_FILE_NAME=DEFAULT_LOG_FILE_NAME,
            LOG_OUTPUT_DIR=DEFAULT_LOG_OUTPUT_DIR,
            RENDER_TO_SCREEN=DEFAULT_RENDER_TO_SCREEN,
        )
        return _conf


def generate_user_config(
    USER_NAME: str,
    D_O_B: date,
    LOGIN_STATUS: bool,
    ACCOUNT_LAST_USED: datetime,
    USER_DB_PATH: Path,
    CONFIG_PATH: Path,
    DB_API: str,
    DB_FILE_NAME: str,
    DB_DIR_PATH: Path,
    DB_ECH0: bool,
    DB_HIDE_PARAMETERS: bool,
    LOGGING_LEVEL: int | str,
    LOG_FILE_NAME: Path,
    LOG_OUTPUT_DIR: Path,
    RENDER_TO_SCREEN: bool,
):
    _conf = UserConfig(
        USER_NAME=USER_NAME,
        D_O_B=D_O_B,
        LOGIN_STATUS=LOGIN_STATUS,
        ACCOUNT_LAST_USED=ACCOUNT_LAST_USED,
        USER_DB_PATH=USER_DB_PATH,
        CONFIG_PATH=CONFIG_PATH,
        DB_API=DB_API,
        DB_FILE_NAME=DB_FILE_NAME,
        DB_DIR_PATH=DB_DIR_PATH,
        DB_ECH0=DB_ECH0,
        DB_HIDE_PARAMETERS=DB_HIDE_PARAMETERS,
        LOGGING_LEVEL=LOGGING_LEVEL,
        LOG_FILE_NAME=LOG_FILE_NAME,
        LOG_OUTPUT_DIR=LOG_OUTPUT_DIR,
        RENDER_TO_SCREEN=RENDER_TO_SCREEN,
    )

    return _conf


def write_config(
    config: AppConfig | UserConfig | None,
    write_as: Literal["toml", "json"] = "toml",
    force_creation: bool = False,
):
    if not (config is None):
        write(
            config.dict(),
            to_file=config.CONFIG_PATH,
            file_extension=write_as,
            force_create=force_creation,
        )


def read_config(
    config: Path | None,
    return_as: Literal["dict", "str", "AppConfig", "UserConfig"] = "dict",
    read_as: Literal["json", "toml"] = "toml",
):
    if not (config is None) and (Path(config).exists()):
        if return_as == "dict":
            return read(from_file=config, file_extension=read_as)
        elif return_as == "str":
            return str(read(from_file=config, file_extension=read_as))
        elif return_as == "AppConfig":
            return AppConfig(read(from_file=config, file_extension=read_as))  # type: ignore
        elif return_as == "UserConfig":
            return UserConfig(**read(from_file=config, file_extension=read_as))  # type: ignore
        else:
            return read(from_file=config, file_extension=read_as)


def create_app_dirs(config: AppConfig, force_recreate: bool = False):
    paths = [
        config.APP_HOME_PATH,
        config.APP_DB_DIR,
        config.APP_LOG_DIR,  # type: ignore
        # config.LOG_OUTPUT_DIR, # I think these must be created while creating DB Object
        # config.DB_DIR_PATH
    ]
    if not force_recreate:
        for path in paths:  # type: ignore
            if not path.exists():  # type: ignore # Dumb Idea
                path.mkdir(parents=True)  # type: ignore
        if not config.CONFIG_PATH.exists():
            config.CONFIG_PATH.touch(exist_ok=False)

    elif force_recreate:
        for path in paths:
            if path.exists():  # type: ignore # Dumb Idea
                if path.is_dir():
                    remove_folder_recursively(path)
                if path.is_file():  # absolutely not needed
                    path.unlink()
            path.mkdir(parents=True)  # type: ignore
        if config.CONFIG_PATH.exists():
            config.CONFIG_PATH.unlink()
        config.CONFIG_PATH.touch(exist_ok=False)


PRE_CONFIGURED_APP_CONFIG: AppConfig = generate_app_config()
