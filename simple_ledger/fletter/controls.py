import flet as ft
import math

from simple_ledger import flet_logger, Logger
from simple_ledger.db import Ledger, LedgerDB
from pprint import pformat


# class PaginatedDataTable(ft.UserControl):
#     PROCEED: bool = False  # the constant that takes charge of giving permission to the build method to work
#     HAS_TITLE: bool = False  # the constant that decides whether to create a table title while building the control
#     DEFAULT_ROWS_PER_PAGE: int = 10

#     def __init__(
#         self,
#         data_table: ft.DataTable | None = None,
#         title: str | None = None,
#         rows_per_page: int | None = None,
#     ) -> None:
#         super().__init__()
#         # self.logger = Logger(
#         #     name="PyLedger.Flet@UserControl",
#         #     custom_name_to_message=f"UserControl@{self.__class__.__name__}",
#         # )
#         # flet_logger.custom_name_to_message = f"UserControl@{self.__class__.__name__}"
#         if (data_table, title, rows_per_page) != (None, None, None):
#             self.data_table: ft.DataTable = data_table
#             self.title: str = title
#             self.rows_per_page = self.DEFAULT_ROWS_PER_PAGE
#             self.PROCEED = True
#             self.HAS_TITLE = True  # hey wait a minute , why did i allow this condition to flow ??? :) <=> Since , I am an Idiotic Emotional Fool

#         elif (
#             ((data_table, title) != (None, None))
#             and (type(rows_per_page) == int)
#             and (rows_per_page >= 1)
#         ):
#             self.data_table: ft.DataTable = data_table
#             self.title: str = title
#             self.rows_per_page = rows_per_page
#             self.PROCEED = True
#             self.HAS_TITLE = True
#         elif data_table == None:
#             self.PROCEED = False  # this will help us to return the default super().__init__() as the return object / value while we execute the build method

#         # build essentials
#         self.CURRENT_PAGE_NUMBER: int = 0
#         self.TOTAL_PAGE_COUNT: int = 0

#         if self.PROCEED:
#             self.TOTAL_PAGE_COUNT = self.total_pages

#             if self.TOTAL_PAGE_COUNT > 0:
#                 self.CURRENT_PAGE_NUMBER = 1

#     @property
#     def data_columns(self) -> list[ft.DataColumn]:
#         # self.logger.info("Proceeding to return the columns in the data table")
#         return self.data_table.columns

#     @property
#     def data_rows(self) -> list[ft.DataRow]:
#         print(pformat(self.data_table.rows, indent=2))
#         return self.data_table.rows

#     @property
#     def paginated_data_rows(self) -> dict[int, list[ft.DataRow]]:
#         _paginated_rows = [
#             self.data_rows[i * self.rows_per_page : (i + 1) * self.rows_per_page]
#             for i in range(
#                 (len(self.data_rows) + self.rows_per_page - 1) // self.rows_per_page
#             )
#         ]
#         paginated_dictionary_for_data_rows: dict[int, list[ft.DataRow]] = {}
#         for page_num in range(len(_paginated_rows)):
#             print(
#                 f"====================================================={page_num+1}=================================="
#             )
#             print(
#                 f"Return Dict:: \n{pformat(paginated_dictionary_for_data_rows, indent=2, sort_dicts=False)}"
#             )
#             paginated_dictionary_for_data_rows[page_num + 1] = _paginated_rows[page_num]
#             print(
#                 "========================================================================================"
#             )

#         else:
#             ...
#         return paginated_dictionary_for_data_rows

#     @property
#     def total_pages(self):
#         return len(list(self.paginated_data_rows.values()))  # remove list after while

#     def set_a_page(self, page_number: int) -> bool:
#         if 1 <= self.CURRENT_PAGE_NUMBER <= self.TOTAL_PAGE_COUNT:
#             print(
#                 "====================================Start - SET A PAGE====================================="
#             )
#             self.CURRENT_PAGE_NUMBER = page_number
#             print(
#                 "====================================End - SET A PAGE====================================="
#             )

#             return True
#         else:
#             return False

#     def set_page(self, delta: int) -> bool:
#         if 0 <= self.CURRENT_PAGE_NUMBER <= self.TOTAL_PAGE_COUNT:
#             print(
#                 "====================================Start - SET A PAGE====================================="
#             )

#             self.CURRENT_PAGE_NUMBER += delta
#             print(
#                 "====================================End - SET A PAGE====================================="
#             )
#             return True
#         else:

#             return False

#     def build(self):
#         def get_to_first_page(e):
#             self.set_a_page(1)
#             page_number_display.value = (
#                 f"Page {self.CURRENT_PAGE_NUMBER}-{self.TOTAL_PAGE_COUNT}"
#             )

#             self.data_table.rows = self.paginated_data_rows[self.CURRENT_PAGE_NUMBER]
#             print(self.CURRENT_PAGE_NUMBER)

#             self.update()

#         def get_to_last_page(e):
#             self.set_a_page(self.TOTAL_PAGE_COUNT)
#             page_number_display.value = (
#                 f"Page {self.CURRENT_PAGE_NUMBER}-{self.TOTAL_PAGE_COUNT}"
#             )

#             self.data_table.rows = self.paginated_data_rows[self.CURRENT_PAGE_NUMBER]
#             print(self.CURRENT_PAGE_NUMBER)

#             self.update()

#         def get_to_previous_page(e):
#             self.set_page(-1)
#             page_number_display.value = (
#                 f"Page {self.CURRENT_PAGE_NUMBER}-{self.TOTAL_PAGE_COUNT}"
#             )

#             self.data_table.rows = self.paginated_data_rows[self.CURRENT_PAGE_NUMBER]
#             print(self.CURRENT_PAGE_NUMBER)

#             self.update()

#         def get_to_next_page(e):
#             self.set_page(1)
#             page_number_display.value = (
#                 f"Page {self.CURRENT_PAGE_NUMBER}-{self.TOTAL_PAGE_COUNT}"
#             )
#             self.data_table.rows = self.paginated_data_rows[self.CURRENT_PAGE_NUMBER]
#             print(self.CURRENT_PAGE_NUMBER)

#             self.update()

#         if self.HAS_TITLE:
#             title_text: ft.Text = ft.Text(
#                 value=str(self.title).title(),
#                 color=ft.colors.YELLOW_ACCENT_700,
#                 style=ft.TextThemeStyle.HEADLINE_MEDIUM,
#                 weight=ft.FontWeight.W_800,
#                 size=25,
#             )
#         first_page_btn: ft.IconButton = ft.IconButton(
#             icon=ft.icons.KEYBOARD_DOUBLE_ARROW_LEFT_ROUNDED,
#             tooltip="Go to First Page",
#             on_click=get_to_first_page,
#         )

#         last_page_btn: ft.IconButton = ft.IconButton(
#             icon=ft.icons.KEYBOARD_DOUBLE_ARROW_RIGHT_ROUNDED,
#             tooltip="Go to Last Page",
#             on_click=get_to_last_page,
#         )

#         previous_page_btn: ft.IconButton = ft.IconButton(
#             icon=ft.icons.KEYBOARD_ARROW_LEFT_ROUNDED,
#             tooltip="Go to Previous Page",
#             on_click=get_to_previous_page,
#         )

#         next_page_btn: ft.IconButton = ft.IconButton(
#             icon=ft.icons.KEYBOARD_ARROW_RIGHT_ROUNDED,
#             tooltip="Go to Next Page",
#             on_click=get_to_next_page,
#         )
#         total_rows_text: ft.Text = ft.Text(
#             value=f"Total Rows: {len(self.data_rows)}",
#             style=ft.TextThemeStyle.DISPLAY_MEDIUM,
#             size=15,
#             weight=ft.FontWeight.BOLD,
#             text_align=ft.TextAlign.END,
#         )
#         page_number_display: ft.Text = ft.Text(
#             value=f"Page {self.CURRENT_PAGE_NUMBER}-{self.TOTAL_PAGE_COUNT}",
#             style=ft.TextThemeStyle.DISPLAY_MEDIUM,
#             size=15,
#             weight=ft.FontWeight.BOLD,
#             text_align=ft.TextAlign.CENTER,
#         )

#         self.data_table.rows = self.paginated_data_rows[self.CURRENT_PAGE_NUMBER]

#         card: ft.Card = ft.Card(
#             content=ft.Container(
#                 content=ft.Column(
#                     controls=[
#                         ft.ResponsiveRow(
#                             controls=[title_text, total_rows_text],
#                             alignment=ft.MainAxisAlignment.CENTER,
#                             # vertical_alignment=ft.CrossAxisAlignment.START,
#                         ),
#                         ft.Column(
#                             controls=[
#                                 self.data_table,
#                                 ft.Row(
#                                     controls=[
#                                         first_page_btn,
#                                         previous_page_btn,
#                                         page_number_display,
#                                         next_page_btn,
#                                         last_page_btn,
#                                     ]
#                                 ),
#                             ],
#                         ),
#                     ],
#                 ),
#                 padding=ft.padding.symmetric(
#                     vertical=15.500000001, horizontal=14.500000001
#                 ),
#             ),
#             elevation=5.65,
#             margin=ft.margin.symmetric(vertical=15.500000001, horizontal=14.500000001),
#         )
#         return card


# DOWNLOAD MY FILE paginated_dt.py
# FROM THIS VIDEO DESCRIPTION


# paginated_dt.py is FOR CREATE YOU DATATABEL
# WITH PAGE AND ROWS

import flet as ft

"""
PaginatedDataTable is based on flet.UserControl.
Feel free to modify it entirely so it could fit your likings and/or needs.

`How to use:`
After initializing the object, you can access the DataTable, DataRow, or DataColumn instances
using the following attributes:
    - `datatable`
    - `datarows`
    - `datacolumns`
"""


class PaginatedDataTable(ft.UserControl):
    # a default number of rows per page to be used in the data table
    DEFAULT_ROW_PER_PAGE = 5

    def __init__(
        self,
        datatable: ft.DataTable,
        table_title: str = "Default Title",
        rows_per_page: int = DEFAULT_ROW_PER_PAGE,
    ):
        """
        A customized user control which returns a paginated data table. It offers the possibility to organize data
        into pages and also define the number of rows to be shown on each page.

        :parameter datatable: a DataTable object to be used
        :parameter table_title: the title of the table
        :parameter rows_per_page: the number of rows to be shown per page
        """
        super().__init__()

        self.dt = datatable
        self.title = table_title
        self.rows_per_page = rows_per_page

        # number of rows in the table
        self.num_rows = len(datatable.rows)
        self.current_page = 1

        # Calculating the number of pages.
        p_int, p_add = divmod(self.num_rows, self.rows_per_page)
        self.num_pages = p_int + (1 if p_add else 0)

        # will display the current page number
        self.v_current_page = ft.Text(
            str(self.current_page),
            tooltip="Double click to set current page.",
            weight=ft.FontWeight.BOLD,
        )

        # textfield to go to a particular page
        self.current_page_changer_field = ft.TextField(
            value=str(self.current_page),
            dense=True,
            filled=False,
            width=40,
            on_submit=lambda e: self.set_page(page=e.control.value),
            visible=False,
            keyboard_type=ft.KeyboardType.NUMBER,
            content_padding=2,
            text_align=ft.TextAlign.CENTER,
        )

        # gesture detector to detect double taps of its contents
        self.gd = ft.GestureDetector(
            content=ft.Row(
                controls=[self.v_current_page, self.current_page_changer_field]
            ),
            on_double_tap=self.on_double_tap_page_changer,
        )

        # textfield to change the number of rows_per_page
        self.v_num_of_row_changer_field = ft.TextField(
            value=str(self.rows_per_page),
            dense=True,
            filled=False,
            width=40,
            on_submit=lambda e: self.set_rows_per_page(e.control.value),
            keyboard_type=ft.KeyboardType.NUMBER,
            content_padding=2,
            text_align=ft.TextAlign.CENTER,
        )

        # will display the number of rows in the table
        self.v_count = ft.Text(weight=ft.FontWeight.BOLD)

        self.pdt = ft.DataTable(columns=self.dt.columns, rows=self.build_rows())

    @property
    def datatable(self) -> ft.DataTable:
        return self.pdt

    @property
    def datacolumns(self) -> list[ft.DataColumn]:
        return self.pdt.columns

    @property
    def datarows(self) -> list[ft.DataRow]:
        return self.dt.rows

    def refresh_button(self, e: ft.ControlEvent):
        self.refresh_data()

    def set_rows_per_page(self, new_row_per_page: str):
        """
        Takes a string as an argument, tries converting it to an integer, and sets the number of rows per page to that
        integer if it is between 1 and the total number of rows, otherwise it sets the number of rows per page to the
        default value

        :param new_row_per_page: The new number of rows per page
        :type new_row_per_page: str
        :raise ValueError
        """
        try:
            self.rows_per_page = (
                int(new_row_per_page)
                if 1 <= int(new_row_per_page) <= self.num_rows
                else self.DEFAULT_ROW_PER_PAGE
            )
        except ValueError:
            # if an error occurs set to default
            self.rows_per_page = self.DEFAULT_ROW_PER_PAGE
        self.v_num_of_row_changer_field.value = str(self.rows_per_page)

        # Calculating the number of pages.
        p_int, p_add = divmod(self.num_rows, self.rows_per_page)
        self.num_pages = p_int + (1 if p_add else 0)

        self.set_page(page=1)
        # self.refresh_data()

    def set_page(self, page: str | int | None = None, delta: int = 0):
        """
        Sets the current page using the page parameter if provided. Else if the delta is not 0,
        sets the current page to the current page plus the provided delta.

        :param page: the page number to display
        :param delta: The number of pages to move forward or backward, defaults to 0 (optional)
        :return: The current page number.
        :raise ValueError
        """
        if page is not None:
            try:
                self.current_page = int(page) if 1 <= int(page) <= self.num_pages else 1
            except ValueError:
                self.current_page = 1
        elif delta:
            self.current_page += delta
        else:
            return
        self.refresh_data()

    def next_page(self, e: ft.ControlEvent):
        """sets the current page to the next page"""
        if self.current_page < self.num_pages:
            self.set_page(delta=1)

    def prev_page(self, e: ft.ControlEvent):
        """set the current page to the previous page"""
        if self.current_page > 1:
            self.set_page(delta=-1)

    def goto_first_page(self, e: ft.ControlEvent):
        """sets the current page to the first page"""
        self.set_page(page=1)

    def goto_last_page(self, e: ft.ControlEvent):
        """sets the current page to the last page"""
        self.set_page(page=self.num_pages)

    def build_rows(self) -> list:
        """
        Returns a slice of indexes, using the start and end values returned by the paginate() function
        :return: The rows of data that are being displayed on the page.
        """
        return self.dt.rows[slice(*self.paginate())]

    def paginate(self) -> tuple[int, int]:
        """
        Returns a tuple of two integers, where the first is the index of the first row to be displayed
        on the current page, and `the second the index of the last row to be displayed on the current page
        :return: A tuple of two integers.
        """
        i1_multiplier = 0 if self.current_page == 1 else self.current_page - 1
        i1 = i1_multiplier * self.rows_per_page
        i2 = self.current_page * self.rows_per_page

        return i1, i2

    def build(self):
        return ft.Card(
            ft.Container(
                ft.Column(
                    [
                        ft.Row(
                            controls=[
                                ft.Text(
                                    self.title, style=ft.TextThemeStyle.HEADLINE_SMALL
                                ),
                                ft.IconButton(
                                    icon=ft.icons.REFRESH_ROUNDED,
                                    tooltip="Refresh Data",
                                    on_click=self.refresh_button,
                                ),
                            ]
                        ),
                        self.pdt,
                        ft.Row(
                            [
                                ft.Row(
                                    controls=[
                                        ft.IconButton(
                                            ft.icons.KEYBOARD_DOUBLE_ARROW_LEFT,
                                            on_click=self.goto_first_page,
                                            tooltip="Go to First Page",
                                        ),
                                        ft.IconButton(
                                            ft.icons.KEYBOARD_ARROW_LEFT,
                                            on_click=self.prev_page,
                                            tooltip="Go to Previous Page",
                                        ),
                                        self.gd,
                                        ft.IconButton(
                                            ft.icons.KEYBOARD_ARROW_RIGHT,
                                            on_click=self.next_page,
                                            tooltip="Go to Next Page",
                                        ),
                                        ft.IconButton(
                                            ft.icons.KEYBOARD_DOUBLE_ARROW_RIGHT,
                                            on_click=self.goto_last_page,
                                            tooltip="Go to Last Page",
                                        ),
                                    ]
                                ),
                                ft.Row(
                                    controls=[
                                        self.v_num_of_row_changer_field,
                                        ft.Text("rows per page"),
                                    ]
                                ),
                                self.v_count,
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                ),
                padding=10,
            ),
            elevation=5,
        )

    def on_double_tap_page_changer(self, e):
        """
        Called when the content of the GestureDetector (gd) is double tapped.
        Toggles the visibility of gd's content.
        """
        self.current_page_changer_field.value = str(self.current_page)
        self.v_current_page.visible = not self.v_current_page.visible
        self.current_page_changer_field.visible = (
            not self.current_page_changer_field.visible
        )
        self.update()

    def refresh_data(self):
        # Setting the rows of the paginated datatable to the rows returned by the `build_rows()` function.
        self.pdt.rows = self.build_rows()
        # display the total number of rows in the table.
        self.v_count.value = f"Total Rows: {self.num_rows}"
        # the current page number versus the total number of pages.
        self.v_current_page.value = f"{self.current_page}/{self.num_pages}"

        # update the visibility of controls in the gesture detector
        self.current_page_changer_field.visible = False
        self.v_current_page.visible = True

        # update the control so the above changes are rendered in the UI
        self.update()

    def did_mount(self):
        self.refresh_data()
