from nicegui import ui
from api.contexts.state import StateContext
from api.road_retreiver import RoadRetreiver
from api.context import AppContextManager
from ui.components.base import BaseComponent
from ui.components.map import RoadMap


class RoadGUI(BaseComponent):
    retreiver = RoadRetreiver()
    context_key = "current_connection"

    def get_container(self):
        return ui.card().style("height: 100%")

    @ui.refreshable
    def render(self):
        if not StateContext.get_value("current_connection"):
            ui.label("Подключения к БД нет. Проверьте его во вкладке \"Подключения\"").style("color:red")
        else:
            try:
                self.retreiver.get_roads()
            except Exception:
                ui.notify("Не удалось подключиться к БД")
                ui.label("Подключения к БД нет. Проверьте его во вкладке \"Подключения\"").style("color:red")
            with self.container:
                with ui.row().style("width:100%"):
                    with ui.column().classes("col-span-2"):
                        self.search_row()
                        self.roads_table = ui.table(
                            columns=[
                                {"name": "id", "label": "ID", "field": "id"},
                                {"name": "name", "label": "Название", "field": "name"},
                            ],
                            rows=self.retreiver.roads,
                            selection="multiple",
                            pagination=10,
                            on_select=lambda e: self.set_selected_id(e.selection),
                        ).style("width: 30rem; table-layout: fixed;")
                    with ui.column().classes("col-span-2"):
                        self.map = RoadMap()

    def set_selected_id(self, rows: list):
        """
        Выбираем Id в гуишной табличке и перезагружаем карту
        """
        ids = [row["id"] for row in rows]
        AppContextManager.context["selected_ids"] = ids
        self.map.change_map_center(ids[-1] if len(ids) > 0 else None)

    def update_table(self, search_text=None):
        """
        Перезагружаем таблицу по поиску
        """
        if search_text is None:
            self.retreiver.get_roads()
        else:
            self.retreiver.get_roads_by_name(search_text)
        self.roads_table.rows = self.retreiver.roads
        ui.update()

    def search_row(self):
        with ui.row().style("width:100%"):
            # with ui.button_group().props("rounded"):
            search_input = ui.input(
                placeholder=" Поиск",
                on_change=lambda: self.update_table(search_input.value),
            ).props("rounded outlined dense")
            with ui.button(on_click=lambda: self.update_table(), color="white").props(
                "rounded"
            ):
                ui.icon("clear")
            # with ui.input(placeholder=" Поиск").props('rounded outlined dense').style('border: none') as search_input:

    # ui.label("Дороги")
    
