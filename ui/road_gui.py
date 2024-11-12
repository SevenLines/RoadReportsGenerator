from nicegui import ui
from api.road_retreiver import RoadRetreiver
from ui.context import context
class RoadGUI:
    retreiver = RoadRetreiver()

    def __init__(self):
        self.retreiver.get_roads()
        self.search_row = self.search_row()
        self.roads_table = ui.table(
            rows=self.retreiver.roads,
            selection='multiple',
            pagination=10,
            on_select=lambda e: self.set_selected_id(e.selection),
        )
    
    def set_selected_id(self,rows:list):
        ids = [row['id'] for row in rows]
        context['selected_id'] = ids

    
    def update_table(self, search_text=None):
        if search_text is None:
            self.retreiver.get_roads()
        else:
            self.retreiver.get_roads_by_name(search_text)
        self.roads_table.rows = self.retreiver.roads
        ui.update()

    def search_row(self):
        with ui.row():
            search_input = ui.input(
                placeholder=' Поиск',
            )
            with ui.button(
                on_click=lambda: self.update_table(search_input.value)
            ):
                ui.icon('search'),
            ui.button(
                'Сбросить',
                on_click=lambda: self.update_table()
            )
            


    # ui.label("Дороги")
    
