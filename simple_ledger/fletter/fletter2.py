import flet as ft

from simple_ledger.db import Ledger, LedgerDB

# from simple_ledger.fletter.controls import PaginatedDataTable


def main(page: ft.Page):
    database = LedgerDB()  # creating database
    # configuring pages
    page.title = "PyLedger"
    page.theme_mode = ft.ThemeMode.DARK

    # !-- Tab ONE
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

    # summary_tab = ft.ListView(auto_scroll=True, expand=1, spacing=10)
    # summary_tab.controls.append(data_table)

    # Tab ONE --!

    # !-- Tab TWO

    summary_tab = ft.Column(
        controls=[data_table],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )

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
            # secondary_column_from.value = ""
            # secondary_column_to.value = ""
            # secondary_column_amount.value = ""
            # secondary_column_description.value = ""
            # secondary_column_tag.value = ""

    ledger_entry_button = ft.TextButton(text="+ Add", on_click=add_entry)

    add_entry_tab = ft.Column(
        [
            secondary_column_from,
            secondary_column_to,
            secondary_column_amount,
            secondary_column_description,
            secondary_column_tag,
            ledger_entry_button,
        ],
        scroll="always",
    )

    # TAB Section
    tab = ft.Tabs(  # Top most selection widget to use
        selected_index=0,
        tabs=[
            ft.Tab(
                icon=ft.icons.SUMMARIZE_OUTLINED,
                text="Summary",
                content=summary_tab,
            ),
            ft.Tab(
                icon=ft.icons.ADD,
                text="Add Entry",
                content=add_entry_tab,
            ),
            ft.Tab(icon=ft.icons.DELETE_ROUNDED, text="Delete Entry"),
        ],
    )

    page.add(tab)


if ft.Page.platform == "android":
    ft.app(target=main, view=ft.WEB_BROWSER, port=9000)
else:
    ft.app(target=main)
