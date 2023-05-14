# from flet import DataTable, ScrollBox
# import flet as ft

# class ScrollableDataTable(DataTable):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self._scroll_box = ScrollBox(content=self, height=kwargs.get('height', '300px'))

#     def show(self):
#         self._scroll_box.show()

# def main(page: ft.Page):
#     page.theme_mode = ft.ThemeMode.DARK

#     page.add(PaginatedDataTable())


# ft.app(target=main)
