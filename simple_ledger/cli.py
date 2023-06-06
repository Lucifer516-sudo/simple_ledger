"""
CLI Version of Simple Ledger
"""
import dataclasses
from datetime import datetime
from pathlib import Path
import typer
from simple_ledger.utils._log import Logger
from simple_ledger.backend.db import LedgerDB, Ledger
from simple_ledger._config import AppConfig as config
from pprint import pformat
from rich import print, table

cli_logger = Logger(name="PyLedger.cli", level=config.APP_LOG_LEVEL)

app = typer.Typer()

db = LedgerDB()
cli_logger.debug(
    f"LEDGER@CLI: Creating Ledger db with default config\n\t{pformat(config.APP_DB_CONFIG, indent=1)}"
)
db.create_table_metadata()


@app.command
def update_config():
    """Updates the ledger config in the _config.py"""
    empty_dict: dict[str, any] = {}
    print(
        "Showing the default config for the App\n[bold yellow italic]NOTE: To Update DB config use update-db-config[/]"
    )
    config_dict = dataclasses.asdict(config)

    key_attribute_pair = list(
        zip(
            [x + 1 for x in range(len(config_dict.keys()))],
            config_dict.values(),
        )
    )
    print(config_dict)

    while True:
        print("Enter the Number To Update the config")

        for value in key_attribute_pair:
            print(f"{value[0]} - {value[1]}")
        typer.prompt("")
    config.update_config(updation_dict=empty_dict)
    # incomplete still


@app.command
def add_entry():
    keys_ = set(dict(Ledger.dict()).keys())
    values_ = []
    for key in keys_:
        values_.append(
            typer.prompt(f"Enter the value for [bold green underline]{key}[/]")
        )
    db.add_ledger_info(ledger=Ledger(**dict(zip(keys_, values_))))
    db.summary(from_=datetime.date(2023, 1, 1), to_=datetime.date(2023, 1, 1))
