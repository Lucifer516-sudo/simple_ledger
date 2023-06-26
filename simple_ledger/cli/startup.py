from simple_ledger.cli import create_app_dirs, console, config, db
from simple_ledger.utils.config.config import write_config


WELCOME_TEXT = f"""
[bold underline yellow]Greetings[/]
WELCOME To,
[bold blue]        ________[/]
[bold blue]        |       |       |[/]
[bold blue]        |       |       |         _______  _______    ______   _______  _______[/]
[bold blue]        |_______| \  /  |        |        |       \  |        |         |      \\ [/]
[bold yellow]        |          \/   |        |_______ |        | |   ___  |_______  |______/ [/]
[bold yellow]        |          /    |        |        |        | |      | |         |      \\ [/]
[bold yellow]        |         /     |_______ |_______ |_______/  |______| |_______  |       \  (R) [/]
"""


def startup(force_clean: bool = False):
    try:
        console.rule("PyLedger - Startup ...")
        console.log("PyLedger Starting ... ")
        console.log("Creating App Related Directories ...")
        create_app_dirs(config, force_recreate=force_clean)
        console.log("Created App Related Directories ...")
        console.rule()
        console.log(f"Writing Config File: {config.CONFIG_PATH}")
        write_config(config, force_creation=force_clean)
        console.rule("PyLedger - Startup Successful ...")
        console.line()
        console.print(
            WELCOME_TEXT,
        )

    except:
        ...


def create_db():
    database = db()
    database.create_data_base_directory_and_file()
    database.create_table_metadata()
