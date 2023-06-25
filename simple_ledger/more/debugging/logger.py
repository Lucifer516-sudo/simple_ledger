import functools
import logging
from collections.abc import Mapping
from pathlib import Path
from typing import Any, Callable
from time import perf_counter
from rich.logging import RichHandler
from simple_ledger.utils.rich_printing._get_console import get_console
from simple_ledger.utils.config.config import PRE_CONFIGURED_APP_CONFIG as CONFIG


class Logger(logging.Logger):
    def __init__(
        self,
        name: str,
        *,
        level: int | str = CONFIG.LOGGING_LEVEL,
        render_to_console: bool = CONFIG.RENDER_TO_SCREEN,
        log_folder: str | Path | None = CONFIG.LOG_OUTPUT_DIR,
        log_file: str | Path | None = CONFIG.LOG_FILE_NAME,  # type: ignore
    ) -> None:  # type: ignore
        super().__init__(name, level)
        self.setLevel(level=level)

        self.current_loggers: list[dict[str, Any]] = []

        if not ((log_file is None) and (log_file is None)):
            self._log_folder = log_folder
            self._log_file = open(str(Path(self._log_folder) / log_file), "wt")  # type: ignore
            self._console_to_write_file = get_console(record=True, file=self._log_file)  # type: ignore

            if isinstance(self._log_folder, str) or isinstance(self._log_folder, Path):
                self._log_folder = Path(self._log_folder)
            if not Path(self._log_folder).exists():  # type: ignore
                Path(self._log_folder).mkdir(parents=True)  # type: ignore

            self.rich_file_handler: RichHandler = RichHandler(
                level=self.level,
                console=self._console_to_write_file,
                rich_tracebacks=True,
                tracebacks_extra_lines=10,
                tracebacks_show_locals=True,
                locals_max_length=500,
                omit_repeated_times=False,
            )

            self.addHandler(self.rich_file_handler)

        self._render_to_console = render_to_console
        if self._render_to_console:
            self._console_to_render = get_console(record=True)

            self.rich_handler: RichHandler = RichHandler(
                level=self.level,
                console=self._console_to_render,
                rich_tracebacks=True,
                tracebacks_extra_lines=10,
                tracebacks_show_locals=True,
                locals_max_length=250,
                omit_repeated_times=False,
            )
            self.addHandler(self.rich_handler)

    def debug(
        self,
        msg: object,
        *args: object,
        exc_info=None,
        stack_info: bool = False,
        stacklevel: int = 3,
        extra: Mapping[str, object] | None = None,
    ) -> None:
        return super().debug(
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra,
        )

    def info(
        self,
        msg: object,
        *args: object,
        exc_info=None,
        stack_info: bool = False,
        stacklevel: int = 3,
        extra: Mapping[str, object] | None = None,
    ) -> None:
        return super().info(
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra,
        )

    def warning(
        self,
        msg: object,
        *args: object,
        exc_info=None,
        stack_info: bool = False,
        stacklevel: int = 3,
        extra: Mapping[str, object] | None = None,
    ) -> None:
        return super().warning(
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra,
        )

    def error(
        self,
        msg: object,
        *args: object,
        exc_info=None,
        stack_info: bool = False,
        stacklevel: int = 3,
        extra: Mapping[str, object] | None = None,
    ) -> None:
        return super().error(
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra,
        )

    def critical(
        self,
        msg: object,
        *args: object,
        exc_info=None,
        stack_info: bool = False,
        stacklevel: int = 3,
        extra: Mapping[str, object] | None = None,
    ) -> None:
        return super().critical(
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra,
        )

    def getChild(self, suffix: str):
        return self.get_logger(f"{super().name}.{suffix}")

    def get_logger(self, name: str):
        # # _l = Logger(name)
        # _l = logging.getLogger(name)
        # _l.setLevel(level=self.level)
        # for handler in self.handlers:
        #     _l.addHandler(handler)
        # return _l
        __logger = Logger(name)
        return __logger

    def catch(self, func: Callable):
        """Catches general exceptions"""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.exception(str(e))

        return wrapper

    def timer(self, func: Callable, msg: str | None = None):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = perf_counter()
            a = func(*args, **kwargs)
            stop = perf_counter()
            if not msg is None:
                self.debug(
                    f"{msg}`{func.__name__}` is:  {round((stop-start)/60, 3)} min [or] {round(stop-start, 3)} sec"
                )
            else:
                self.debug(
                    f"Processing time for the function `{func.__name__}` is:  {round((stop-start)/60, 3)} min [or] {round(stop-start, 3)} sec"
                )
            return a

        return wrapper
