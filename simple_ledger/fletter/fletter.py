import flet as ft
from simple_ledger.db import Ledger, LedgerDB

# from flet import Page, TextField, ElevatedButton


def main(page: ft.Page):
    """
    + Tabs
        +-- Add Entry ( Show recently added view)
        +-- Remove Entry
        +-- Update Entry
        +-- Summary (Data Table)
    """
    database = LedgerDB()  # creating database
    # configuring pages
    page.title = "PyLedger"
    page.theme_mode = ft.ThemeMode.DARK
    # page.appbar = ft.AppBar(leading=)

    # from , to , amount, des , tag
    secondary_column_from = ft.TextField(
        label="From", autofocus=True, height=50
    )

    secondary_column_to = ft.TextField(label="To", height=50)
    secondary_column_amount = ft.TextField(label="Amount", height=50)
    secondary_column_description = ft.TextField(label="Description", height=50)
    secondary_column_tag = ft.Dropdown(
        label="Tag",
        options=[
            ft.dropdown.Option(key="CREDIT", text="CREDIT"),
            ft.dropdown.Option(key="DEBIT", text="DEBIT"),
        ],
    )

    def add_entry(e):
        for val in [
            secondary_column_from,
            secondary_column_to,
            secondary_column_amount,
            secondary_column_description,
            secondary_column_tag,
        ]:
            if not val.value:
                print("None  | False")
        else:
            entry = Ledger(
                from_person=str(secondary_column_from.value),
                to_person=str(secondary_column_to.value),
                description=str(secondary_column_description.value),
                amount=float(secondary_column_amount.value),
                tag=secondary_column_tag.value.upper(),
            )
            database.add_ledger_info(ledger=entry)
            secondary_column_entry_added.value = f"Added Entry"
            secondary_column_from.value = ""
            secondary_column_to.value = ""
            secondary_column_amount.value = ""
            secondary_column_description.value = ""
            secondary_column_tag.value = ""
            required_data = []

            for data in database.read_ledger_info():
                required_data.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(value=str(data.id))),
                            ft.DataCell(ft.Text(value=str(data.from_person))),
                            ft.DataCell(ft.Text(value=str(data.to_person))),
                            ft.DataCell(ft.Text(value=str(data.amount))),
                            ft.DataCell(ft.Text(value=str(data.tag))),
                        ]
                    )
                )

            page.update()

    secondary_column_button_to_add_entry = ft.ElevatedButton(
        text="Add Entry", on_click=add_entry
    )
    secondary_column_entry_added = ft.Text(value="No entry Added Yet")
    required_data = []

    for data in database.read_ledger_info():
        required_data.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(value=str(data.id))),
                    ft.DataCell(ft.Text(value=str(data.from_person))),
                    ft.DataCell(ft.Text(value=str(data.to_person))),
                    ft.DataCell(ft.Text(value=str(data.amount))),
                    ft.DataCell(ft.Text(value=str(data.tag))),
                ]
            )
        )

    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("S.No"), numeric=True),
            ft.DataColumn(label=ft.Text("From")),
            ft.DataColumn(label=ft.Text("To")),
            ft.DataColumn(label=ft.Text("Amount"), numeric=True),
            ft.DataColumn(label=ft.Text("Mode")),
        ],
        rows=required_data,
        expand=True,
    )
    secondary_column = ft.Column(
        [
            secondary_column_from,
            secondary_column_to,
            secondary_column_amount,
            secondary_column_description,
            secondary_column_tag,
            secondary_column_button_to_add_entry,
            secondary_column_entry_added,
            data_table,
        ],
    )
    page.add(secondary_column)


ft.app(
    target=main,
)  # view=ft.WEB_BROWSER, port=8085)
