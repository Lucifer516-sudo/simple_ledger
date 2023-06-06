"""This module provides a custom logger class that enables colorized console logging and file logging with rotation.

Classes:
    ColoredFormatter:
        A custom formatter class that adds colors to log messages.

    Logger:
        A custom logger class that provides colorized console logging and file logging with rotation.

Functions:
    create_multi_loggers:
        Creates multiple logger instances for specified logger names.

Attributes:
    No module-level attributes are defined in this module.

Usage:
    To create a single logger instance, create an instance of the Logger class with a name, logging level, and optionally a log file and other logging options. To create multiple logger instances for specified logger names, call the create_multi_loggers function with a list of logger names.

Example:

    # Create a logger instance with name "my_logger" and log level "DEBUG"
    logger = Logger(name="my_logger", level=logging.DEBUG)

    # Log a debug message
    logger.debug("This is a debug message")

    # Create multiple logger instances for specified logger names
    create_multi_loggers(loggers=["sqlalchemy.orm", "sqlalchemy.dialects", "sqlalchemy.pool", "sqlalchemy.engine"])

Classes:

    ColoredFormatter:
        A custom formatter class that adds colors to log messages.

        Methods:
            __init__(self, *args, **kwargs):
                Initializes the ColoredFormatter instance.

            format(self, record):
                Formats a log record by adding colors to the message based on the log level.

        Attributes:
            colors:
                A dictionary that maps log levels to ANSI escape codes for colorizing the log message.

            reset:
                An ANSI escape code that resets the color of the log message.

    Logger:
        A custom logger class that provides colorized console logging and file logging with rotation.

        Methods:
            __init__(
                self,
                name: str,
                level=logging.INFO,
                log_file: Optional[str] = None,
                log_dir: Union[str,Path,None] = None,
                backup_count: int = 5,
                max_size: int = 1048576,
            ):
                Initializes the Logger instance.

            debug(self, message, *args, **kwargs):
                Logs a debug message.

            info(self, message, *args, **kwargs):
                Logs an info message.

            warning(self, message, *args, **kwargs):
                Logs a warning message.

            error(self, message, *args, **kwargs):
                Logs an error message.

            critical(self, message, *args, **kwargs):
                Logs a critical message.

            exception(self, message, *args, exc_info=True, **kwargs):
                Logs an exception message.

        Attributes:
            logger_name:
                The name of the logger.

            logger:
                The logger instance.

            formatter:
                The formatter instance used for formatting log messages.

            console_handler:
                The console handler instance used for logging messages to the console.

            file_handler:
                The file handler instance used for logging messages to a file.

            colors:
                A dictionary that maps log levels to ANSI escape codes for colorizing the log message.

            reset:
                An ANSI escape code that resets the color of the log message.

Functions:

    create_multi_loggers:
        Creates multiple logger instances for specified logger names.

        Arguments:
            loggers:
                A list of logger names.

        Returns:
            None.

        Side Effects:
            - Creates logger instances with names based on the items in the loggers list.
            - Assigns global variables with names based on the items in the loggers list, each containing an instance of the Logger class with the corresponding logger name.

Attributes:

    No module-level attributes are defined in this module.
"""

from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
from typing import Optional, Self, Type, Union

from sqlmodel import Field
from simple_ledger._config import AppConfig as config


class ColoredFormatter(logging.Formatter):
    """
    A custom formatter class that adds colors to log messages.

    Attributes:
        colors (dict): A dictionary that maps logging levels to ANSI color codes.
        reset (str): The ANSI reset code.
    """

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        # self.colors = {
        #     "DEBUG": "\033[1;34m",
        #     "INFO": "\033[1;32m",
        #     "WARNING": "\033[1;33m",
        #     "ERROR": "\033[1;31m",
        #     "CRITICAL": "\033[1;41m",
        # }
        # self.reset = "\033[0m"

    def format(self, record):
        """
        Format a log record.

        Args:
            record (LogRecord): The log record to format.

        Returns:
            str: The formatted log record.
        """

        levelname = record.levelname
        self.backup_level_name = record.levelname
        self.backup_name = record.levelname
        # if levelname in self.colors:
        levelname_color = f"[{levelname:<8}]"
        record.levelname = levelname_color
        name = record.name
        # if not self.custom_name == None:
        # record.message = self.custom_name + ": ``" + record.message
        name_color = f"{name:<10}"
        record.name = name_color
        return super().format(record)

    def __exit__(self, record):
        record.name = self.backup_name
        record.levelname = self.backup_level_name


class Logger:
    """
    A custom logger class that provides colorized console logging and file logging with rotation.

    Attributes:
        logger_name (str): The name of the logger.
        logger (logging.Logger): The logger object.
        formatter (ColoredFormatter): The formatter object.
        console_handler (logging.StreamHandler): The console handler object.
        file_handler (RotatingFileHandler): The file handler object.
    """

    def __init__(
        self,
        *,
        name: str,
        custom_name_to_message: str = "",
        level=config.APP_LOG_LEVEL,
        log_file: Optional[str] = config().APP_LOG_FILE_NAME,
        log_dir: Union[str, Path, None] = config().APP_LOG_DIR,
        backup_count: int = 5,
        max_size: int = 10485760 * 50,  # 50 MB
    ):
        """
        Initialize the logger with a name, logging level, and optionally a log file and other logging options.

        Args:
            name (str): The name of the logger.
            level (int): The logging level. Defaults to logging.INFO.
            log_file (str, optional): The name of the log file. Defaults to None.
            log_dir (Union[str,Path,None], optional): The path to the log directory. Defaults to None.
            backup_count (int, optional): The number of backup log files to keep. Defaults to 5.
            max_size (int, optional): The maximum size of the log file in bytes. Defaults to 1048576.
        """

        self.logger_name = name
        self.custom_name_to_message = custom_name_to_message
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        if not self.custom_name_to_message == "":
            self.formatter = ColoredFormatter(
                "[%(asctime)s] %(levelname)s `%(name)s` : "
                + str(self.custom_name_to_message)
                + " >> "
                + "%(message)s",
                # custom_name_to_message=self.custom_name_to_message,
            )
        else:
            self.formatter = ColoredFormatter(
                "[%(asctime)s] %(levelname)s `%(name)s` : %(message)s"
            )

        self.console_handler = logging.StreamHandler()
        self.console_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.console_handler)

        if log_dir == None:
            log_dir = Path(config().APP_LOG_DIR)
            log_dir.mkdir(parents=True, exist_ok=True)
            if log_file == None:
                log_file = f"{self.logger_name.split('.')[0]}__{str(datetime.now())[:13].replace(' ','_')}.log"
        else:
            log_dir.mkdir(parents=True, exist_ok=True)

        self.file_handler = RotatingFileHandler(
            log_dir / log_file,
            backupCount=backup_count,
            maxBytes=max_size,
        )
        if not self.custom_name_to_message == "":
            file_formatter = logging.Formatter(
                "[%(asctime)s] %(levelname)s `%(name)s` : "
                + str(self.custom_name_to_message)
                + " >> "
                + "%(message)s",
            )
        else:
            file_formatter = logging.Formatter(
                "[%(asctime)s] %(levelname)s `%(name)s` : %(message)s",
            )
        self.file_handler.setFormatter(file_formatter)
        self.logger.addHandler(self.file_handler)

    @staticmethod
    def create_child(*, parent_logger: logging.Logger, child_name: str):
        parent_logger_name = parent_logger.name
        return Logger(name=str(parent_logger_name + "." + child_name))

    def debug(self, message, *args, **kwargs):
        """Log a debug message."""
        self.logger.debug(message, *args, **kwargs)

    def info(self, message, *args, **kwargs):
        """Log an info message."""
        self.logger.info(message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        """Log a warning message."""
        self.logger.warning(message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        """Log an error message."""
        self.logger.error(message, *args, **kwargs)

    def critical(self, message, *args, **kwargs):
        """Log a critical message."""
        self.logger.critical(message, *args, **kwargs)

    def exception(self, message, *args, exc_info=True, **kwargs):
        """Log an exception message."""
        self.logger.exception(message, *args, exc_info=exc_info, **kwargs)
