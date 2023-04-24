"""
The above code defines a custom logging system in Python with console and file handlers, custom
formatters, and the ability to add more loggers.
"""

from collections.abc import Mapping
import datetime
import logging
from logging import LogRecord
from pathlib import Path
from typing import Any, Type
from colorama import Fore, Back, Style


class ConsoleFormatter(logging.Formatter):
    """
    This is a custom formatter for Python's logging module that adds color and formatting to log
    messages.

    Args:
      fmt (str | None): A string that specifies the format of the log message.
      datefmt (str | None): The `datefmt` parameter is a string that specifies the format of the date
    and time information in the log messages. It uses the same format codes as the `strftime()` function
    in Python's standard library. If `datefmt` is not provided, the default format is used.
      style: The `style` parameter is a string that specifies the format style for the log messages. It
    defaults to `"%"`, which is the classic Python logging format style. Other options include `"{"` and
    `"["`, which are alternative format styles. Defaults to %
      validate (bool): The `validate` parameter is a boolean flag that determines whether the logging
    configuration should be validated or not. If set to `True`, the logging configuration will be
    validated and any errors or warnings will be raised as exceptions. If set to `False`, the logging
    configuration will not be validated and any errors. Defaults to True
      defaults (Mapping[str, Any] | None): The `defaults` parameter is an optional argument that can be
    passed to the constructor of a logging formatter. It is a dictionary-like object that contains
    default values for the formatter's attributes. These default values will be used if the
    corresponding attribute is not set in the log record being formatted.
    """

    def __init__(
        self,
        fmt: str | None = None,
        datefmt: str | None = None,
        style="%",
        validate: bool = True,
        *,
        defaults: Mapping[str, Any] | None = None,
    ) -> None:
        """
        The `super().__init__(fmt, datefmt, style, validate, defaults=defaults)` line is calling the
        constructor of the parent class (`logging.Formatter`) with the provided arguments (`fmt`,
        `datefmt`, `style`, `validate`, `defaults`). This initializes the formatter object with the
        specified format and date format strings, as well as any default values for the formatter's
        attributes.
        """
        super().__init__(fmt, datefmt, style, validate, defaults=defaults)

        self.colors_for_levels: dict[str, str] = {
            "DEBUG": Fore.BLUE,
            "INFO": Fore.GREEN,
            "WARNING": Back.LIGHTGREEN_EX + Fore.LIGHTRED_EX,
            "ERROR": Back.GREEN + Fore.LIGHTMAGENTA_EX,
            "CRITICAL": Back.LIGHTYELLOW_EX + Fore.RED,
        }

        self.RESET_CODE: str = Style.RESET_ALL
        self.BRIGHT: str = Style.BRIGHT
        self.DIM: str = Style.DIM
        self.NORMAL: str = Style.NORMAL

    def format(self, record: LogRecord) -> str:
        """
        This code block is defining the `format` method of the `ConsoleFormatter` class, which is a custom
        formatter for Python's logging module that adds color and formatting to log messages.
        """

        if (
            not record.msg.split(":")[0].isspace()
            and len(record.msg.split(":")[0]) > 1
        ):
            custom_name: str = f"{Back.LIGHTRED_EX}{self.BRIGHT}{Fore.MAGENTA}{record.msg.split(':')[0].strip().title()}{self.RESET_CODE}"

        logger_level: str = f"{self.BRIGHT}{self.colors_for_levels[record.levelname]}{record.levelname}{self.RESET_CODE}"
        record.levelname: str = logger_level
        record.coloured_custom_name: str = custom_name

        return super().format(record)


class FileFormatter(logging.Formatter):
    """
    This is a Python function that formats a log record by extracting a custom name from the log message
    and adding color to it.

    Args:
        fmt (str | None): A string that specifies the format of the log message.
        datefmt (str | None): The `datefmt` parameter is used to specify the format of the date and time
    in the log message. It is a string that can contain various format codes that are replaced with the
    corresponding values when the log message is formatted. If `datefmt` is not specified, the default
    format is used
        style: The `style` parameter is used to specify the format style for the log messages. It defaults
    to the `'%'` style, which is the classic Python logging format style. Other options include `'{'`
    and `'$'` styles. Defaults to %
        validate (bool): A boolean parameter that determines whether the format string should be validated
    or not. If set to True, the format string will be checked for errors and warnings during
    initialization. If set to False, no validation will be performed. Defaults to True
        defaults (Mapping[str, Any] | None): The `defaults` parameter is an optional argument that can be
    passed to the constructor of a logging formatter. It is a dictionary-like object that contains
    default values for the formatter's attributes. These default values will be used if the
    corresponding attribute is not set in the log record being formatted.
    """

    def __init__(
        self,
        fmt: str | None = None,
        datefmt: str | None = None,
        style="%",
        validate: bool = True,
        *,
        defaults: Mapping[str, Any] | None = None,
    ) -> None:
        """
        `super().__init__(fmt, datefmt, style, validate, defaults=defaults)` is calling the
        constructor of the parent class (`logging.Formatter`) with the provided arguments (`fmt`,
        `datefmt`, `style`, `validate`, `defaults`). This initializes the formatter object with the
        specified format and date format strings, as well as any default values for the formatter's
        attributes.
        """
        super().__init__(fmt, datefmt, style, validate, defaults=defaults)

    def format(self, record: LogRecord) -> str:
        """
        This code block is extracting a custom name from the log message and adding color to it. It
        checks if the first part of the log message (before the colon) is not empty or just
        whitespace, and if its length is greater than 1. If these conditions are met, it extracts
        the custom name by splitting the log message at the colon and taking the first part,
        stripping any leading or trailing whitespace, and converting it to title case. It then sets
        the `coloured_custom_name` attribute of the log record to the custom name with color
        formatting applied. Finally, it calls the `format` method of the parent class
        (`logging.Formatter`) with the modified log record to generate the final formatted log
        message.
        """
        if (
            not record.msg.split(":")[0].isspace()
            and len(record.msg.split(":")[0]) > 1
        ):
            custom_name: str = f"{record.msg.split(':')[0].strip().title()}"
        record.coloured_custom_name: str = custom_name

        return super().format(record)


class Logger(object):
    # _instance = None

    # def __new__(cls, *args, **kwargs) -> :
    #     if cls._instance is None:
    #         cls._instance:  = super().__new__(cls, *args, **kwargs)
    #     return cls._instance

    def __init__(
        self,
        name="ledger",
        level=logging.DEBUG,
        stdout: bool = True,
        file_path: str | Path | None = None,
    ) -> None:
        """
        This is a constructor function for a custom logger that can output logs to both stdout and a
        file.

        Args:
          name: The name of the logger. Defaults to ledger
          level: The logging level to be set for the logger. It defaults to logging.DEBUG.
          stdout (bool): A boolean parameter that determines whether log messages should be printed to
        the console or not. If True, log messages will be printed to the console. If False, log messages
        will only be written to the file specified in the file_path parameter. Defaults to True
          file_path (str | Path | None): The file path where the log messages will be saved. If set to
        None, the log messages will not be saved to a file.
        """
        self.logger = logging.getLogger(name)
        logging.root = self.logger
        self.logger.setLevel(level=level)
        if all([stdout, file_path]):
            self.logger.addHandler(
                logging.StreamHandler().setFormatter(
                    ConsoleFormatter(
                        fmt="[%(levelname)s] [%(custom_name)s] : %(message)s"
                    )
                )
            )
            self.logger.addHandler(
                logging.FileHandler(filename=file_path).setFormatter(
                    fmt=FileFormatter(
                        "[%(asctime)s] [%(levelname)s] [%(custom_name)s] -- %(message)s"
                    )
                )
            )

        if (stdout == False) and (file_path != None):
            self.logger.addHandler(
                logging.FileHandler(filename=file_path).setFormatter(
                    fmt=FileFormatter(
                        "[%(asctime)s] [%(levelname)s] [%(custom_name)s] -- %(message)s"
                    )
                )
            )

        if (stdout == True) and (file_path == None):
            self.logger.addHandler(
                logging.StreamHandler().setFormatter(
                    ConsoleFormatter(
                        fmt="[%(levelname)s] [%(custom_name)s] : %(message)s"
                    )
                )
            )

    def modify_the_new_ones(
        self,
        logger: logging.Logger,
        *,
        stdout: bool = True,
        file_path: str | Path | None = None,
    ) -> None:
        """
        This function modifies the logging configuration based on the provided parameters for logging to
        stdout and/or a file.

        Args:
          logger (logging.Logger): A logging.Logger object that is used to log messages.
          stdout (bool): A boolean parameter that determines whether the log messages should be printed
        to the console or not. If True, the log messages will be printed to the console. If False, the
        log messages will not be printed to the console. Defaults to True
          file_path (str | Path | None): The path to the file where the log messages will be written. If
        None, the log messages will not be written to a file.
        """

        if all([stdout, file_path]):
            logger.addHandler(
                logging.StreamHandler().setFormatter(
                    ConsoleFormatter(
                        fmt="[%(levelname)s] [%(custom_name)s] : %(message)s"
                    )
                )
            )
            logger.addHandler(
                logging.FileHandler(filename=file_path).setFormatter(
                    fmt=FileFormatter(
                        "[%(asctime)s] [%(levelname)s] [%(custom_name)s] -- %(message)s"
                    )
                )
            )

        if (stdout == False) and (file_path != None):
            logger.addHandler(
                logging.FileHandler(filename=file_path).setFormatter(
                    fmt=FileFormatter(
                        "[%(asctime)s] [%(levelname)s] [%(custom_name)s] -- %(message)s"
                    )
                )
            )

        if (stdout == True) and (file_path == None):
            logger.addHandler(
                logging.StreamHandler().setFormatter(
                    ConsoleFormatter(
                        fmt="[%(levelname)s] [%(custom_name)s] : %(message)s"
                    )
                )
            )

    def add_more_loggers(
        self,
        logger_names: str | list[str] = None,
        *,
        stdout: bool = True,
        file_path: str | Path | None = None,
    ) -> None:
        """
        This function adds new loggers and modifies their settings based on the specified parameters.

        Args:
          logger_names (str | list[str]): A string or a list of strings representing the names of the
        loggers to be created or modified.
          stdout (bool): A boolean parameter that determines whether log messages should be printed to
        the console (standard output) in addition to being written to a file. If set to True, log
        messages will be printed to the console. If set to False, log messages will only be written to
        the file specified by the file_path. Defaults to True
          file_path (str | Path | None): The `file_path` parameter is a string or a `Path` object that
        specifies the path to the file where the logs will be saved. If it is set to `None`, the logs
        will not be saved to a file.
        """
        if not isinstance(logger_names, str):
            for name in logger_names:
                logging.getLogger(name)
                self.modify_the_new_ones(
                    logging.getLogger(name), stdout=stdout, file_path=file_path
                )

        if isinstance(logger_names, str):
            logging.getLogger(name)
            self.modify_the_new_ones(
                logging.getLogger(name), stdout=stdout, file_path=file_path
            )
