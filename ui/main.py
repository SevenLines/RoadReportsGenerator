from api.utils import open_finder_macos
from ui.components.report_form import ReportFormGUI
from ui.components.road_gui import RoadGUI
from ui.components.lists.last_reports_list import LastReportsListComponent
from ui.components.sidebar import sidebar
from nicegui import ui
from ui.views.connection_view import connection_view
from ui.views.template_view import template_view
ui.add_head_html('<link href="https://unpkg.com/eva-icons@1.1.3/style/eva-icons.css" rel="stylesheet" />')



def main_content():
    with ui.row().style("width: 100%; height: 100%"):
        with ui.column().style("width: 75rem;height: 100%"):
            RoadGUI()
        with ui.column().style("width: 15rem;height: 100%"):
            ReportFormGUI()
        # with ui.column().style("width: 15rem;height: 100%"):
        #     last_reports_list()

def main_page():
    sidebar(
        tabs={
            "Генерация": "home",
            "Шаблоны": "settings",
            "Подключения": "lan",
            }, 
        panels={
            "Генерация": main_content,
            "Шаблоны": template_view,
            "Подключения": connection_view
            },
        # default={"Генерация":main_content}
        )
    
