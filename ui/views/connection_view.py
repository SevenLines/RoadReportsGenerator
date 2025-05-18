from nicegui import ui
from ui.components.lists.access_connections import AccessSavedConnectionComponent
from ui.components.forms.saved_file_form import SaveConnectionFileForm
from ui.components.forms.db_connection_form import DBConnectionFormComponent
from ui.components.lists.db_connections import SavedConnectionComponent
from api.contexts.state import StateContext
from api.utils import choose_file
def connection_view():

    with ui.row().classes("col-span-full"):
        with ui.column().classes("col-span-2"):
            with ui.tabs().classes('w-full') as tabs:
                ms_sql = ui.tab('MS SQL')
                ms_access = ui.tab('MS Access')
            with ui.tab_panels(tabs, value=ms_sql).classes('w-full'):
                with ui.tab_panel(ms_sql):
                    DBConnectionFormComponent()
                with ui.tab_panel(ms_access):
                    SaveConnectionFileForm()
            

        with ui.column().classes("col-span-2"):
            ui.label("Сохраненные подключения")
            SavedConnectionComponent()
            AccessSavedConnectionComponent()
            

