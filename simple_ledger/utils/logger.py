from collections.abc import Mapping
import logging
from logging import LogRecord
import os
from typing import Any
from textwrap import shorten
from pathlib import Path
from datetime import datetime


class ConsoleFormatter(logging.Formatter):
    def __init__(
        self,
        fmt: str | None = "%(levelname)s",
        datefmt: str | None = None,  # "[%x %X %p]",
        style="%",
        validate: bool = True,
        *,
        defaults: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(fmt, datefmt, style, validate, defaults=defaults)

    def format(self, record: LogRecord) -> str:
        return super().format(record)


class ConsoleHandler(logging.StreamHandler):
    def emit(self, record: LogRecord) -> None:
        record.raw_name: str = record.name
        record.raw_levelname: str = record.levelname
        record.raw_msg: str = record.msg
        record.raw_datetime: str = datetime.now().strftime("%x %X %p")
        record.raw_filename: str = record.filename
        record.raw_lineno: int = record.lineno

        # need to shorten the message that is being shown to console for that, we need
        # - column width
        # - prefix like asctime,... etc,... length(width)
        # -- if the msg length is higher than the available space then shorten it
        formatted_raw_level_name: str = record.raw_levelname + str(
            " " * (10 - len(record.raw_levelname))
        )
        col_one: str = f"{record.raw_datetime} | {formatted_raw_level_name} | "
        # col_two: str = f"{record.msg} | "
        _temp = record.raw_filename + ":" + str(record.raw_lineno)
        col_three: str = f"{_temp}"

        col_one_size: int = int(len(col_one))
        col_three_size: int = int(len(col_three))
        total_col_size: int = int(os.get_terminal_size()[0])

        if len(record.msg) >= (
            total_col_size - (col_one_size + col_three_size) + 5
        ):  # +5 is due to the presence of ` ... `
            formatted_msg_size: int = total_col_size - (col_one_size + col_three_size)
            record.formatted_msg: str = (
                shorten(record.msg, formatted_msg_size)[:-5] + " ... "
            )
            col_two: str = f"{record.formatted_msg} | "
        elif len(record.msg) < (total_col_size - (col_one_size + col_three_size)):
            number_of_spaces: int = total_col_size - (
                col_one_size + len(record.msg) + col_three_size + 5
            )
            record.formatted_msg: str = record.msg + " " * number_of_spaces
            col_two: str = f"{record.formatted_msg} | "

        else:
            col_two: str = f"{record.msg} | "

        record.levelname = col_one + col_two + col_three
        return super().emit(record)


class FileFormatter(logging.Formatter):
    def __init__(
        self,
        fmt: str | None = "%(levelno)s",
        datefmt: str | None = None,
        style="%",
        validate: bool = True,
        *,
        defaults: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(fmt, datefmt, style, validate, defaults=defaults)

    def format(self, record: LogRecord) -> str:
        record.levelno = f"{record.raw_datetime} | {record.raw_levelname:<10} | {str(record.raw_msg).ljust(100)} | ({record.pathname}:{record.raw_lineno}) => `{record.module:^10}` with logger :: {record.name}"
        return super().format(record)


class Logger(logging.Logger):
    def __init__(
        self,
        name: str,
        level: int | str = logging.DEBUG,
        render_to_console: bool = True,
        log_to_path: str | None | Path = None,
    ) -> None:
        super().__init__(name, level)

        self.some_handlers_to_use = []

        if render_to_console:
            # Console Logging
            console_formatter = ConsoleFormatter()
            console_handler = ConsoleHandler()
            console_handler.setFormatter(console_formatter)
            self.addHandler(console_handler)
            self.some_handlers_to_use.append(console_handler)

        if not log_to_path is None:
            # File Logging
            file_formatter = FileFormatter()
            file_handler = logging.FileHandler(log_to_path, mode="a")
            file_handler.setFormatter(file_formatter)
            self.addHandler(file_handler)
            self.some_handlers_to_use.append(file_handler)

        if not render_to_console and log_to_path is None:
            file_formatter = FileFormatter()
            file_handler = logging.FileHandler("unIntentionallyCreatedLog.log")
            file_handler.setFormatter(file_formatter)
            self.addHandler(file_handler)

        # Notifying that we have started logging
        self.info("Logging Started ...".center(75, "-"))

    def debug(self, msg: object, *args, **kwargs) -> None:
        return super().debug(msg, *args, **kwargs)

    def info(self, msg: object, *args, **kwargs) -> None:
        return super().info(msg, *args, **kwargs)

    def warning(self, msg: object, *args, **kwargs) -> None:
        return super().warning(msg, *args, **kwargs)

    def error(self, msg: object, *args, **kwargs) -> None:
        return super().error(msg, *args, **kwargs)

    def critical(self, msg: object, *args, **kwargs) -> None:
        return super().critical(msg, *args, **kwargs)

    def get_logger(self, name: str):
        _logger = logging.getLogger(name)
        _logger.setLevel(self.level)
        for h in self.some_handlers_to_use:
            _logger.addHandler(h)
        return _logger

    def __exit__(self):
        self.info("Logging Stopped...".center(75, "-"))


# l = Logger("Test", log_to_path="test_222.log")

# from time import sleep

# for i in range(20):
#     l.debug(f"Debug Msg => {i}")
#     l.info(f"Info Msg => {i}")
#     l.warning(f"Warning Msg => {i}")
#     l.error(f"Error Msg => {i}")
#     l.critical(f"Critical Msg => {i}")
#     l.info("-" * 50)
#     sleep(0.4)
