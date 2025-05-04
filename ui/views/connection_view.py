from nicegui import ui
from ui.components.forms.connection_form import ConnectionFormComponent
from ui.components.lists.connection_history import SavedConnectionComponent
from api.managers.implementations import ConnectionManager
from api.contexts.state import StateContext

def connection_view():

    with ui.row().classes("col-span-full"):
        with ui.column().classes("col-span-2"):
            with ui.tabs().classes('w-full') as tabs:
                ms_sql = ui.tab('MS SQL')
                ms_access = ui.tab('MS Access')
            with ui.tab_panels(tabs, value=ms_sql).classes('w-full'):
                with ui.tab_panel(ms_sql):
                    ConnectionFormComponent()
                with ui.tab_panel(ms_access):
                    ui.upload(label="Загрузить файл").style("width: 30rem")
            

        with ui.column().classes("col-span-2"):
            ui.label("Сохраненные подключения")
            SavedConnectionComponent()
            