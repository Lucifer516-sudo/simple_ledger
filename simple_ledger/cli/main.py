import typer
from simple_ledger.cli.startup import startup, create_db, db
from simple_ledger.cli.login import login
from simple_ledger.cli.add_entry import add_entry

from simple_ledger.cli import (
    table,
    console,
    rich_table,
    rich_table_data,
    rich_column,
    rich_row,
)

app = typer.Typer()


@app.command()
def start(force: bool = False):
    startup(force)


@app.command()
def create_database():
    create_db()


@app.command()
def add_new_entry():
    data = table(**add_entry())
    database = db()
    try:
        if database.add_ledger_info(ledger=data):
            console.print("Added New Entry ...")
            console.rule("Success")
    except Exception as e:
        console.print_exception()
        console.rule()


@app.command()
def show_ledger_entries():
    database = db()
    data = database.read_ledger_info()

    columns = [
        rich_column("S.No"),
        rich_column("Entry Added On", justify="left"),
        rich_column("Customer Name", justify="left"),
        rich_column(
            "Amount Charged",
            justify="right",
            convert_to_money=True,
            money_symbol="Rs.",
        ),
    ]
    total_transactions = len(data)
    total_credit: float = float(sum([datum.amount_charged for datum in data]))
    rows = []

    for datum in data:
        rows.append(
            rich_row(
                values=[
                    datum.id,
                    datum.transaction_noted_on,
                    datum.customer_name,
                    datum.amount_charged,
                ]
            )
        )

    table_data = rich_table_data(title="WORK DONE", columns=columns, rows=rows)
    console.print(rich_table(table_data))
    console.print(
        f"Total Number of Transactions: [bold italic]{total_transactions}[/]\nTotal Credits: [bold green]Rs.[/] [bold italic blue]{total_credit:,}[/]"
    )
    console.rule()
    console.line()


@app.command()
def run():
    menu = """
[bold underline blue ]MENU[/]
[bold italic green]0[/].) [bold blue italic underline]This Menu Screen 
[bold italic green]1[/].) [bold yellow]Welcome screen and startup[/]
[bold italic green]2[/].) [bold yellow]Add New Entry to Book[/]
[bold italic green]3[/].) [bold yellow]Show all Entries[/]
[bold italic green]4[/].) [bold yellow][bold italic red]Exit[/] the App[/]
"""
    while True:
        console.print(menu, justify="center")
        option: int = int(
            console.input(
                "Enter your [bold]choice[/]([blue bold] 1 / 2 / 3 / 4 / 0 [/]) (Default: 0): "
            )
        )

        match option:
            case 1:
                startup()
            case 2:
                data = table(**add_entry())
                database = db()
                try:
                    if database.add_ledger_info(ledger=data):
                        console.print("Added New Entry ...")
                        console.rule("Success")
                except Exception as e:
                    console.print_exception()
                    console.rule()
            case 3:
                database = db()
                data = database.read_ledger_info()

                columns = [
                    rich_column("S.No"),
                    rich_column("Entry Added On", justify="left"),
                    rich_column("Customer Name", justify="left"),
                    rich_column(
                        "Amount Charged",
                        justify="right",
                        convert_to_money=True,
                        money_symbol="Rs.",
                    ),
                ]
                total_transactions = len(data)
                total_credit: float = float(
                    sum([datum.amount_charged for datum in data])
                )
                rows = []

                for datum in data:
                    rows.append(
                        rich_row(
                            values=[
                                datum.id,
                                datum.transaction_noted_on,
                                datum.customer_name,
                                datum.amount_charged,
                            ]
                        )
                    )

                table_data = rich_table_data(
                    title="WORK DONE", columns=columns, rows=rows
                )
                console.print(rich_table(table_data))
                console.print(
                    f"Total Number of Transactions: [bold italic]{total_transactions}[/]\nTotal Credits: [bold green]Rs.[/] [bold italic blue]{total_credit:,}[/]"
                )
                console.rule()
                console.line()

            case 4:
                console.print(
                    "[bold green]Thank You so much for using ... \nHave a nice day ...[/]",
                    justify="center",
                )
                exit()
            case 0:
                pass
            case _:
                pass


if __name__ == "__main__":
    app()
