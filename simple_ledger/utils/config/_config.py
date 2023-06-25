import logging
from datetime import date, datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseSettings, Field

from simple_ledger.utils.file_handling.file_ops import write, read


class AppInfo(BaseSettings):
    """Holds Data Related to The CLI App"""

    NAME: str
    VERSION: tuple[int, ...]
    RELEASE: str
    APP_HOME_PATH: Path
    APP_DB_DIR: Path
    APP_LOG_DIR: Path
    CONFIG_PATH: Path


class AppDBConfig(BaseSettings):
    """Contains information related to DB"""

    DB_API: str  # for less dependency and more combatibility
    DB_FILE_NAME: str
    DB_DIR_PATH: Path
    DB_ECH0: bool  # else will produce blah blahs
    DB_HIDE_PARAMETERS: bool  # else will show data


class LoggingConfig(BaseSettings):
    """Contains information related to Logging"""

    LOGGING_LEVEL: int | str
    LOG_FILE_NAME: str
    LOG_OUTPUT_DIR: Path
    RENDER_TO_SCREEN: bool


class UserInfo(BaseSettings):
    """User Info class"""

    USER_NAME: str
    D_O_B: date
    LOGIN_STATUS: bool
    ACCOUNT_LAST_USED: datetime
    USER_DB_PATH: Path
    CONFIG_PATH: Path


class UserDBConfig(AppDBConfig):
    """User DB COnfig"""

    ...


class AppConfig(LoggingConfig, AppDBConfig, AppInfo):
    """Contains AppConfig Record,
    Such as,
        -> AppInfo
        -> AppDBConfig
        -> LoggingConfig
    """

    ...


class UserConfig(LoggingConfig, UserDBConfig, UserInfo):
    """Contains UserConfig Record,
    Such as,
        -> UserInfo
        -> UserDBConfig
        -> LoggingConfig
    """

    ...
