import flet as ft
import math
from simple_ledger import flet_logger, ledger_logger, Logger
from simple_ledger.db import LedgerDB


class PaginatedDataTable(ft.UserControl):
    DEFAULT_ROW_PER_PAGE: int = 10

    def __init__(
        self,
        columns: list[ft.DataColumn] | None = None,
        rows: list[ft.DataRow] | None = None,
        table_title: str | None = None,
        rows_per_page: int = DEFAULT_ROW_PER_PAGE,
    ):
        self.columns: list[ft.DataColumn] | None = columns
        self.rows: list[ft.DataRow] | None = rows
        self.table_title: str | None = table_title
        self.rows_per_page: int = rows_per_page

        self.current_page: int = 1  # default page
        self.total_pages: int = 1  # total number of pages
        self.paginated_rows = self.paginated_rows

        # controls

        self.page_number_display: ft.Text = ft.Text(
            value=f"{self.current_page}/{self.total_pages}",
            style=ft.TextThemeStyle.DISPLAY_MEDIUM,
            italic=True,
        )
        self.next_page_button: ft.IconButton = ft.IconButton(
            icon=ft.icons.KEYBOARD_ARROW_RIGHT_ROUNDED,
            tooltip="Next Page",
            on_click=self._on_next_page(),
        )
        self.prev_page_button: ft.IconButton = ft.IconButton(
            icon=ft.icons.KEYBOARD_ARROW_LEFT_ROUNDED,
            tooltip="Previous Page",
            on_click=self._on_prev_page(),
        )

        self.first_page_button: ft.IconButton = ft.IconButton(
            icon=ft.icons.KEYBOARD_DOUBLE_ARROW_LEFT_ROUNDED,
            tooltip="First Page",
            on_click=self._on_first_page,
        )
        self.last_page_button: ft.IconButton = ft.IconButton(
            icon=ft.icons.KEYBOARD_DOUBLE_ARROW_RIGHT_ROUNDED,
            tooltip="Last Page",
            on_click=self._on_last_page,
        )

        self.title_text: ft.Text = ft.Text(
            value=self.table_title.title(), style=ft.TextThemeStyle.TITLE_MEDIUM
        )
        self.refresh_data_button: ft.IconButton = ft.IconButton(
            icon=ft.icons.REFRESH_SHARP,
            tooltip="Refresh Data",
            on_click=self._on_refresh(),
        )

        self.data_table = ft.DataTable(
            columns=self.columns,
            heading_text_style=ft.TextStyle(
                size=10, italic=True, decoration=ft.TextDecoration.UNDERLINE
            ),
            heading_row_color=ft.colors.BACKGROUND,
            show_bottom_border=True,
        )

        if self.is_rows == True:
            if len(list(self.paginated_rows.keys())) >= 1:
                self.data_table.rows = self.paginated_rows[1]
                self.update()

    @property
    def is_columns(self) -> bool:
        if self.columns != None:
            return True
        else:
            return False

    @property
    def is_rows(self) -> bool:
        if self.rows != None:
            return True
        else:
            return False

    @property
    def total_rows(self) -> int | None:
        if self.is_rows == True:
            return len(self.rows)
        else:
            return None

    def paginate_rows(self) -> dict[int, list[ft.DataRow]] | None:
        if self.total_rows != None:
            _ = {}

            _temp_sub_list: list[
                ft.DataRow
            ] = []  # create a list to paginated chunks (rows)
            shallow_copy_of_rows = self.rows.copy()  # making a shallow copy of list
            for chunk_index in range(0, self.total_rows, self.rows_per_page):
                _temp_sub_list = shallow_copy_of_rows[
                    chunk_index : chunk_index + self.rows_per_page
                ]

            for _page_num in range(self.total_rows):
                _[_page_num + 1] = _temp_sub_list[
                    _page_num
                ]  # creating the paginated data dict , that has the page num and the rows

            return _
        else:
            return None

    @property
    def get_total_pages(self) -> int | None:
        float_part, int_part = math.modf(self.total_rows / self.rows_per_page)
        if float_part > 0.0:
            int_part += 1
            return int_part
        elif (float_part < 0.0) or (float_part == 0):
            return int_part
        else:
            return None

    def set_page(self, delta: int = 0):
        self.current_page += delta
        self.page_number_display.value = f"{self.current_page}/{self.total_pages}"
        self.data_table.rows = self.paginated_rows[self.current_page]
        self.update()

    def set_a_page(self, page_number: int = 1):
        self.current_page = 1
        self.page_number_display.value = f"{self.current_page}/{self.total_pages}"
        self.data_table.rows = self.paginated_rows[self.current_page]
        self.update()

    def _on_next_page(self, e: ft.ControlEvent):
        if self.current_page <= self.total_pages:
            self.set_page(delta=1)

    def _on_prev_page(self, e: ft.ControlEvent):
        if self.current_page >= 1:
            self.set_page(delta=-1)

    def _on_first_page(self, e: ft.ControlEvent):
        if self.total_pages >= 1:
            self.set_a_page(page_number=1)

    def _on_last_page(self, e: ft.ControlEvent):
        if self.total_pages >= 1:
            self.set_a_page(page_number=self.total_pages)

    def _on_refresh(self):
        db = LedgerDB()
        required_data = []

        for data in db.read_ledger_info():
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
        self.rows = required_data
        self.paginated_rows = self.paginate_rows()
        self.set_a_page(page_number=self.current_page)
        self.update()

    def build(self):
        card: ft.Card = ft.Card(
            ft.Container(
                ft.Column(
                    controls=[
                        self.title_text,
                        self.refresh_data_button,
                        self.data_table,
                        ft.Row(controls=[]),
                    ]
                )
            )
        )


def main(page: ft.Page):
    cols = [
        ft.DataColumn(ft.Text("S.NO")),
        ft.DataColumn(ft.Text("Name")),
    ]
    rows = []

    for i in range(76):
        rows.append(
            ft.DataRow(
                cells=[ft.DataCell(ft.Text(f"{i+1}.")), ft.DataCell(ft.Text("God"))]
            )
        )
    # table = ft.DataTable(columns=cols, rows=rows)
    page.theme_mode = ft.ThemeMode.DARK
    page.add(PaginatedDataTable(columns=cols, rows=rows))


ft.app(target=main)
