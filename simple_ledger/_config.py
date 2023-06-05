# The `Config` class is a constructor function that initializes various attributes for a Python
# application and provides methods for creating, showing, and loading configuration files.

from datetime import date, datetime
from pathlib import Path
from typing import Any, Type
import toml


class Config:
    """
    The `Config` class is a constructor function that initializes various attributes for a Python
    application and provides methods for creating, showing, and loading configuration files.
    """

    __count__: int = 0  # `__count__: int = 0` is defining a class attribute `__count__` with an initial value of 0. This
    # attribute is used to keep track of the number of log files created by the application, to ensure
    # that each log file has a unique name.

    def __init__(
        self,
        APP_NAME: str | None = None,
        APP_VERSION: str | int | float | None = None,
        APP_HOME: str | Path | None = None,
        APP_DB_DIR: str | Path | None = None,
        APP_LOG_DIR: str | Path | None = None,
        APP_LOG_FILE_NAME: str | None = None,
        APP_LOG_LEVEL: str | int | None = None,
        APP_DB_NAME: str | None = None,
        APP_DB_DIR_NAME: str | None = None,
        APP_LOG_DIR_NAME: str | None = None,
        APP_HOME_NAME: str | None = None,
        APP_DB_CONFIG: dict[str, Any] | None = None,
        APP_CONFIG_PATH: Path | str | None = None,
        APP_LOGGER: list[str] | None = None,
    ) -> None:
        """
        This is a constructor function that initializes various attributes for a Python application.

        Args:
          APP_NAME (str | None): A string representing the name of the application.
          APP_VERSION (str | int | float | None): The version number of the application. It can be a
        string, integer or float. If not provided, it defaults to "0.0.1".
          APP_HOME (str | Path | None): The directory path where the application's files and data will
        be stored.
          APP_DB_DIR (str | Path | None): The directory where the application's database files will be
        stored.
          APP_LOG_DIR (str | Path | None): The directory where log files will be stored for the
        application.
          APP_LOG_FILE_NAME (str | None): The name of the log file that will be created by the
        application. If not provided, it will be generated based on the current date and time, and a
        count to ensure uniqueness.
          APP_LOG_LEVEL (str | int | None): This parameter specifies the logging level for the
        application. It can be set to a string value such as "DEBUG", "INFO", "WARNING", "ERROR", or
        "CRITICAL", or an integer value representing the logging level. If this parameter is not
        provided, the default logging level is set to
          APP_DB_NAME (str | None): The name of the database for the application.
          APP_DB_DIR_NAME (str | None): This parameter is a string that represents the name of the
        directory where the application's database files will be stored. If this parameter is not
        provided, the default value "Ledger-DB" will be used.
          APP_LOG_DIR_NAME (str | None): This parameter is a string or Path object that represents the
        name of the directory where log files will be stored for the application. If this parameter is
        not provided, the default value "Ledger-Logs" will be used.
          APP_HOME_NAME (str | None): The name of the application's home directory. If not provided, it
        defaults to the APP_NAME.
          APP_DB_CONFIG (dict[str, Any] | None): A dictionary containing configuration options for the
        database, including the database API to use, the name of the database, the directory where the
        database should be stored, whether to enable echoing of SQL statements, and whether to hide
        parameters in SQL statements.
          APP_CONFIG_PATH (Path | str | None): A string or Path object representing the path to the
        configuration file for the application. If not provided, it defaults to the "config.toml" file
        located in the APP_HOME directory.
          APP_LOGGER (list[str] | None): APP_LOGGER is a list of strings that contains the names of the
        loggers that will be used in the application. These loggers will be used to log different events
        and messages in the application. If this parameter is not provided, the default loggers used
        will be "PyLedger" and "
        """
        self.APP_NAME = APP_NAME
        self.APP_VERSION = APP_VERSION
        self.APP_HOME = APP_HOME
        self.APP_DB_DIR = APP_DB_DIR
        self.APP_LOG_DIR = APP_LOG_DIR
        self.APP_LOG_FILE_NAME = APP_LOG_FILE_NAME
        self.APP_LOG_LEVEL = APP_LOG_LEVEL
        self.APP_DB_NAME = APP_DB_NAME
        self.APP_DB_DIR_NAME = APP_DB_DIR_NAME
        self.APP_LOG_DIR_NAME = APP_LOG_DIR_NAME
        self.APP_HOME_NAME = APP_HOME_NAME
        self.APP_DB_CONFIG = APP_DB_CONFIG
        self.APP_CONFIG_PATH = APP_CONFIG_PATH
        self.APP_LOGGER = APP_LOGGER

        if self.APP_NAME == None:
            self.APP_NAME = "PyLedger"

        if self.APP_VERSION == None:
            self.APP_VERSION = "0.0.1"

        if self.APP_HOME_NAME == None:
            self.APP_HOME_NAME = self.APP_NAME

        if self.APP_HOME == None:
            self.APP_HOME = Path().home() / str(
                self.APP_HOME_NAME + "_" + self.APP_VERSION
            )

        if self.APP_DB_DIR_NAME == None:
            self.APP_DB_DIR_NAME = "Ledger-DB"

        if self.APP_LOG_DIR_NAME == None:
            self.APP_LOG_DIR_NAME = "Ledger-Logs"

        if self.APP_DB_DIR == None:
            self.APP_DB_DIR = (
                self.APP_HOME / self.APP_DB_DIR_NAME / datetime.now().strftime("%Y")
            )

        if self.APP_LOG_FILE_NAME == None:
            mtimes = [
                file_name.lstat().st_mtime
                for file_name in Path(self.APP_LOG_DIR).glob("*.log")
            ]

            if len(mtimes) != 0:
                max_time = max(mtimes)
                for file_name in Path(APP_LOG_DIR).glob("*.log"):
                    if max_time == file_name.lstat().st_mtime:
                        self.__count__ = int(
                            int(str(file_name).replace(".log", "").split("_")[-1]) + 1
                        )  # increasing the count

            self.APP_LOG_FILE_NAME = (
                self.APP_NAME
                + "__"
                + str(date.today()).replace(" ", "_")
                + "_"
                + str(self.__count__)
                + ".log"
            )

        if self.APP_LOG_DIR == None:
            self.APP_LOG_DIR = Path(
                self.APP_HOME
                / self.APP_LOG_DIR_NAME
                / datetime.now().strftime("%Y")
                / datetime.now().strftime("%B").upper()
                / str(str("DAY_") + str(datetime.now().day))
                / str(str("HOUR_") + str(datetime.now().hour))
            )

        if self.APP_LOG_LEVEL == None:
            self.APP_LOG_LEVEL = "DEBUG"

        if self.APP_DB_CONFIG == None:
            self.APP_DB_CONFIG = {
                "db_api": "sqlite",
                "db_name": self.APP_NAME + ".db",
                "db_dir": self.APP_DB_DIR,
                "echo": True,
                "hide_parameters": False,
            }

        if self.APP_CONFIG_PATH == None:
            self.APP_CONFIG_PATH = self.APP_HOME / "config.toml"

        if self.APP_LOGGER == None:
            self.APP_LOGGER = [
                "PyLedger",
                "flet",
            ]

    @property
    def default(self):
        """
        This is a Python function that returns a dictionary containing various properties related to an
        application.

        Returns:
          A dictionary containing various properties related to the application such as its name,
        version, configuration path, home directory, database configuration, log level, log file name,
        log directory name, log directory, and loggers.
        """
        return {
            "APP": {
                "NAME": self.APP_NAME,
                "VERSION": self.APP_VERSION,
                "CONFIG_PATH": self.APP_CONFIG_PATH,
            },
            "APP_HOME": {
                "HOME": self.APP_HOME,
                "HOME_NAME": self.APP_HOME_NAME,
            },
            "APP_DB": {
                "DB_CONFIG": self.APP_DB_CONFIG,
                "DB_NAME": self.APP_DB_NAME,
                "DB_DIR_NAME": self.APP_DB_DIR_NAME,
                "DB_DIR": self.APP_DB_DIR,
            },
            "APP_LOG": {
                "LOG_LEVEL": self.APP_LOG_LEVEL,
                "LOG_FILE_NAME": self.APP_LOG_FILE_NAME,
                "LOG_DIR_NAME": self.APP_LOG_DIR_NAME,
                "LOG_DIR": self.APP_LOG_DIR,
            },
            "LOGGERS": self.APP_LOGGER,
        }

    def create_config(self):
        """
        This function creates a configuration file by writing the output of the "show_config" method to
        a file.
        """
        conf = str(self.show_config())

        with open(self.APP_CONFIG_PATH, "w") as file:
            file.write(conf)

    def show_config(self):
        """
        The function returns a TOML-formatted string representation of a default configuration.

        Returns:
          The `show_config` method is returning a TOML formatted string representation of the `default`
        attribute of the object.
        """
        return toml.dumps(self.default)

    def load_config(self, fpath: Path | str | None = None) -> Type[toml.load]:
        """
        This function loads a TOML configuration file from a given path or a default path.

        Args:
          fpath (Path | str | None): The `fpath` parameter is a Path object, a string representing a file
        path, or None. It is used to specify the path to the configuration file that needs to be loaded. If
        `fpath` is None, the default configuration file path `APP_CONFIG_PATH` is used.

        Returns:
          the output of the `toml.load()` function, which is a dictionary containing the parsed contents of
        the TOML file specified by the `fpath` argument. The return type is `Type[toml.load]`, which is not
        a valid type annotation. It should be changed to `Dict[str, Any]` to indicate that the function
        returns a dictionary with string keys
        """
        if fpath == None:
            fpath = str(self.APP_CONFIG_PATH)
        return toml.load(fpath)
