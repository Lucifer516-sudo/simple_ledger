from collections.abc import Mapping
from logging import LogRecord
from pathlib import Path
from typing import Any
import logging
from logging.handlers import TimedRotatingFileHandler


class StreamFormatter(logging.Formatter):
    def __init__(
        self,
        fmt: str
        | None = "%(asctime)s [%(levelname)-10s] %(message)-56s | %(filename)s:%(lineno)d",
        datefmt: str | None = "[%x %X %p]",
        style: str = "%",
        validate: bool = True,
        *,
        defaults: Mapping[str, Any] | None = None
    ) -> None:
        super().__init__(fmt, datefmt, style, validate, defaults=defaults)

    def format(self, record: LogRecord) -> str:
        return super().format(record)


class FileFormatter(logging.Formatter):
    def __init__(
        self,
        fmt: str
        | None = "%(asctime)s [%(levelname)-15s] (%(module)s|%(funcName)s) - %(message)-150s [%(pathname)s:%(lineno)d]",
        datefmt: str | None = "[%x %X %p | week: %U/53 ]",
        style: str = "%",
        validate: bool = True,
        *,
        defaults: Mapping[str, Any] | None = None
    ) -> None:
        super().__init__(fmt, datefmt, style, validate, defaults=defaults)

    def format(self, record: LogRecord) -> str:
        return super().format(record)


class Logger(logging.Logger):
    def __init__(
        self,
        name: str,
        level: int | str = 0,
        *,
        render_to_console: bool = True,
        log_to_path: str | Path | None = None
    ) -> None:
        super().__init__(name, level)

        self.setLevel(level=level)
        self._render_to_console = render_to_console
        self._log_to_path = log_to_path

        if self._render_to_console:
            self.stream_handler: logging.StreamHandler = logging.StreamHandler()
            self.stream_handler.setFormatter(StreamFormatter())
            self.addHandler(self.stream_handler)
        if not (self._log_to_path is None):
            if isinstance(self._log_to_path, str or Path):
                self._log_to_path = Path(self._log_to_path)
            if not self._log_to_path.exists():
                self._log_to_path.touch()
            # else:
            #     self._log_to_path = Path(
            #         str(self._log_to_path)[:-4]
            #         + str(int(str(self._log_to_path)[:-4][:-2]) + 1)
            #         + ".log"
            #     )

            self.file_handler = TimedRotatingFileHandler(
                self._log_to_path,
            )
            self.file_handler.setFormatter(FileFormatter())
            self.addHandler(self.file_handler)
        self.info("===================Logging started===================")

    def debug(
        self,
        msg: object,
        *args: object,
        exc_info=None,
        stack_info: bool = False,
        stacklevel: int = 3,
        extra: Mapping[str, object] | None = None
    ) -> None:
        return super().debug(
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra
        )

    def info(
        self,
        msg: object,
        *args: object,
        exc_info=None,
        stack_info: bool = False,
        stacklevel: int = 3,
        extra: Mapping[str, object] | None = None
    ) -> None:
        return super().info(
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra
        )

    def warning(
        self,
        msg: object,
        *args: object,
        exc_info=None,
        stack_info: bool = False,
        stacklevel: int = 3,
        extra: Mapping[str, object] | None = None
    ) -> None:
        return super().warning(
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra
        )

    def error(
        self,
        msg: object,
        *args: object,
        exc_info=None,
        stack_info: bool = False,
        stacklevel: int = 3,
        extra: Mapping[str, object] | None = None
    ) -> None:
        return super().error(
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra
        )

    def critical(
        self,
        msg: object,
        *args: object,
        exc_info=None,
        stack_info: bool = False,
        stacklevel: int = 3,
        extra: Mapping[str, object] | None = None
    ) -> None:
        return super().critical(
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra
        )

    def get_loggers(self, name: str):
        _l = logging.getLogger(name)
        _l.setLevel(self.level)
        for i in self.handlers:
            _l.addHandler(i)
        return _l

    def __del__(self):
        self.info("==============Log Finished==============")
