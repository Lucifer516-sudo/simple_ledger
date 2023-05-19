import flet as ft
from simple_ledger import flet_logger, ledger_logger, Logger


class PaginatedDataTable(ft.UserControl):
    def __init__(
        self,
        columns: list[ft.DataColumn] | None = None,
        rows: list[ft.DataRow] | None = None,
        default_number_of_rows: int = 10,
    ):
        super().__init__()

        self.columns: list[ft.DataColumn] | None | list[str] = columns
        self.rows: list[ft.DataRow] | None | list[list[str]] = rows
        self.default_no_of_rows: int = default_number_of_rows
        self.current_page_number: int = 0
        flet_logger.info(f"Creating CustomControl: `Paginated Data Table`")

    @property
    def total_pages(self) -> int:
        if (self.rows != None) and (len(self.rows) > self.default_no_of_rows):
            flet_logger.info("Returning Total Number of Pages")
            flet_logger.debug(
                f"Number of rows > 0 (!None) => Rows: {self.rows} & Default Rows: {self.default_no_of_rows}"
            )
            return len(self.rows) // self.default_no_of_rows
        else:
            return 1

    @property
    def paginated_rows(self) -> dict[int, list[ft.DataRow]] | None:
        # using list comprehension
        if (self.rows != None) and (len(self.rows) > 0):
            flet_logger.info("Creating Paginated Rows")
            _paginated_rows: list[ft.DataRow] = [
                self.rows[
                    i * self.default_no_of_rows : (i + 1) * self.default_no_of_rows
                ]
                for i in range(
                    (len(self.rows) + self.default_no_of_rows - 1)
                    // self.default_no_of_rows
                )
            ]
            flet_logger.debug(
                f"Splitted Rows into paginated rows \nPaginated Row: {len(_paginated_rows)}"
            )

            paginated_data: dict[int, list[ft.DataRow]] = {}

            for page_num in range(len(_paginated_rows)):
                paginated_data[page_num + 1] = _paginated_rows[page_num]
                flet_logger.info("Creating Paginated Data Dict")
                flet_logger.debug(
                    f"Page {page_num+1} => {len(_paginated_rows[page_num])}"
                )
            flet_logger.info("Returning Paginated Data")
            return paginated_data
        else:
            flet_logger.warning(f"Unable To Create Paginated data")
            flet_logger.critical(
                f"Rows => {self.rows}\nPaginated Rows => {_paginated_rows}\nPaginated Data => {paginated_data}"
            )
            return None

    def build(self):
        def _on_increase(e):
            self.current_page_number += 1
            if self.current_page_number < self.total_pages:
                flet_logger.info("Increasing the Page")
                flet_logger.debug(
                    f"Current Page => {self.current_page_number}\nTotal Page => {self.total_pages}\nPage Display Value => {page_number_display.value}"
                )
                page_number_display.value = (
                    f"{self.current_page_number} of {self.total_pages}"
                )
                try:
                    table.rows = self.paginated_rows[self.current_page_number]
                    flet_logger.debug(f"Updating Table Rows")
                except Exception as e:
                    flet_logger.exception(f"Encountered Exception: \n{e}")
                self.update()
            else:
                flet_logger.info("Not Increasing the Page")
                flet_logger.debug(
                    f"Current Page => {self.current_page_number}\nTotal Page => {self.total_pages}\nPage Display Value => {page_number_display.value}"
                )

        def _on_decrease(e):
            self.current_page_number -= 1
            if self.current_page_number > 0:
                flet_logger.info("Decreasing the Page")
                flet_logger.debug(
                    f"Current Page => {self.current_page_number}\nTotal Page => {self.total_pages}\nPage Display Value => {page_number_display.value}"
                )
                page_number_display.value = (
                    f"{self.current_page_number} of {self.total_pages}"
                )
                try:
                    table.rows = self.paginated_rows[self.current_page_number]
                    flet_logger.debug(f"Updating Table Rows")
                except Exception as e:
                    flet_logger.exception(f"Encountered Exception: \n{e}")
                self.update()
            else:
                flet_logger.info("Not Decreasing the Page")
                flet_logger.debug(
                    f"Current Page => {self.current_page_number}\nTotal Page => {self.total_pages}\nPage Display Value => {page_number_display.value}"
                )

        container: ft.Container = ft.Container(bgcolor=ft.colors.YELLOW_300)

        table: ft.DataTable = ft.DataTable(
            divider_thickness=1,
        )
        table.columns = self.columns

        increase_button: ft.OutlinedButton = ft.OutlinedButton(
            icon=ft.icons.SKIP_NEXT_OUTLINED,
            on_click=_on_increase,
        )
        decrease_button: ft.OutlinedButton = ft.OutlinedButton(
            icon=ft.icons.SKIP_PREVIOUS_OUTLINED,
            on_click=_on_decrease,
        )
        page_number_display: ft.Text = ft.Text(
            value=f"0 of 0",
            style=ft.TextThemeStyle.LABEL_SMALL,
        )

        if len(self.rows) > 0:
            self.current_page_number = 1
            page_number_display.value = (
                f"{self.current_page_number} of {self.total_pages}"
            )
            table.rows = self.paginated_rows[self.current_page_number]
        container_row_inside_column: ft.Row = ft.Row(
            controls=[
                decrease_button,
                page_number_display,
                increase_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        container_column: ft.Column = ft.Column(
            controls=[
                table,
                container_row_inside_column,
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        )
        return container_column


def main(page):
    col = [ft.DataColumn(ft.Text("Sno")), ft.DataColumn(ft.Text("Name"))]
    rows = []
    for i in range(100):
        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(f"{i+1}.")),
                    ft.DataCell(ft.Text("God")),
                ]
            )
        )
    page.add(PaginatedDataTable(columns=col, rows=rows))


ft.app(target=main)
