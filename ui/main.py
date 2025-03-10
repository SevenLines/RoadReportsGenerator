from api.utils import open_finder_macos
from ui.report_form import ReportFormGUI
from ui.road_gui import RoadGUI
from ui.components.last_reports_list import last_reports_list
from nicegui import ui


def main_page():
    with ui.header():
        ui.label("Дороги")
        ui.button(icon="folder", on_click=lambda: open_finder_macos())
    with ui.row().style("width: 100%; height: 100%"):
        with ui.column().style("width: 75rem;height: 100%"):
            RoadGUI()
        with ui.column().style("width: 15rem;height: 100%"):
            ReportFormGUI()
        with ui.column().style("width: 15rem;height: 100%"):
            last_reports_list()
