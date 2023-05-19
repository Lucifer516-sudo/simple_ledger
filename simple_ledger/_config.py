from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any


@dataclass
class AppConfig:
    __count__: int = 0
    APP_NAME: str = "PyLedger"
    APP_VERSION: str = "0.0.1"
    APP_HOME: Path = Path().home() / str(APP_NAME + "_" + APP_VERSION)
    APP_LOG_DIR: Path = (
        APP_HOME
        / "LEDGER_LOGS"
        / datetime.now().strftime("%Y")
        / datetime.now().strftime("%B").upper()
        / str(datetime.now().hour)
    )
    APP_LOG_DIR.mkdir(parents=True, exist_ok=True)
    mtimes = []
    for file_name in Path(APP_LOG_DIR).glob(
        "*.log"
    ):  # finding all log files and their mtimes
        mtimes.append(file_name.lstat().st_mtime)
    __count__ = 0

    if len(mtimes) != 0:
        max_time = max(mtimes)
        for file_name in Path(APP_LOG_DIR).glob("*.log"):
            if max_time == file_name.lstat().st_mtime:
                __count__ = (
                    int(str(file_name).replace(".log", "").split("_")[-1]) + 1
                )  # increasing the count

    APP_LOG_FILE_NAME: str = (
        APP_NAME
        + "__"
        + str(date.today()).replace(" ", "_")
        + "_"
        + str(__count__)
        + ".log"
    )
    APP_LOG_LEVEL: str | int = "DEBUG"
    APP_DB_DIR: Path = APP_HOME / "LEDGER_DB" / datetime.now().strftime("%Y")

    APP_DB_CONFIG: dict[str, Any] = field(default_factory=dict)

    def __init__(self):
        self.APP_DB_CONFIG = {
            "db_api": "sqlite",
            "db_name": self.APP_NAME + ".db",
            "db_dir": self.APP_DB_DIR,
            "echo": True,
            "hide_parameters": False,
        }

    def update_config(self, updation_dict: dict[str, Any]):
        for name, attribute in list(updation_dict.items()):
            setattr(AppConfig, name, attribute)
