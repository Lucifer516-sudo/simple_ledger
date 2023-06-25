from typing import Callable
from rich.table import Table, box
from dataclasses import dataclass, asdict


@dataclass
class Column:
    """
    The code is defining a `Column` data class using the `@dataclass` decorator.
    """

    value: str
    justify: str = "center"
    append_str: str | None = None
    apply_function: Callable | None = None
    convert_to_money: bool = False
    money_symbol: str | None = None


@dataclass
class Row:
    """
    The code is defining a `Row` data class using the `@dataclass` decorator. The `Row` class has two
    attributes: `values` and `style`.
    """

    values: list[str | int | float]
    style: str = "italic cyan"


@dataclass
class TableData:
    title: str
    columns: list[Column]
    rows: list[Row]
    expand: bool = False


def rich_table(data: TableData):
    """
    The function `rich_table` creates a rich table object from a given `TableData` object, with options
    for expanding and formatting data.

    Args:
      data (TableData): The input parameter `data` is of type `TableData`, which is a custom class that
    contains information about a table, including its title, columns, rows, and various formatting
    options.

    Returns:
      The function `rich_table` is returning a `Table` object.
    """

    table = Table(
        title=data.title,
        expand=data.expand,
        box=box.HEAVY,
    )
    for column in data.columns:
        column_index: int = data.columns.index(column)  # maybe use set instead
        for row in data.rows:
            row_index: int = data.rows.index(row)
            if not isinstance(row.values[column_index], str):
                row.values[column_index] = str(
                    row.values[column_index]
                )  # force type casting
            if not (column.apply_function is None):
                row.values[column_index] = column.apply_function(
                    row.values[column_index]
                )
            elif not (
                (column.convert_to_money is False) and (column.money_symbol is None)
            ):
                formatted_value = float(row.values[column_index])
                formatted_value = round(formatted_value, 2)

                if len(str(formatted_value).split(".")[-1]) == 1:
                    row.values[
                        column_index
                    ] = f"{column.money_symbol} {''.join(str(formatted_value).split('.')[:-1])}.00"

                else:
                    row.values[
                        column_index
                    ] = f"{column.money_symbol} {str(formatted_value)}"

            else:
                ...

    for column in data.columns:
        table.add_column(column.value, justify=column.justify.lower())

    for row in data.rows:
        table.add_row(*row.values, style=row.style)

    return table


data = TableData(
    title="Ledger Entry 0f 2023",
    columns=[
        Column(value="S.No"),
        Column(value="Name", justify="left"),
        Column(
            value="Amount in Rs.",
            justify="right",
            convert_to_money=True,
            money_symbol="Rs",
        ),
        Column(value="Mode", justify="right"),
    ],
    rows=[
        Row(values=["1.", "Vengat", 1000000.0601010101111, "Credit"]),
        Row(values=["2.", "Logu", 10.012, "Credit"]),
        Row(values=["3.", "Vengat", 1121200.012, "Credit"]),
        Row(values=["4.", "Vengat", 101221100.012, "Credit"]),
        Row(values=["5.", "Sakthi", 1.012, "Credit"]),
    ],
)

from rich import print


print(rich_table(data=data))
