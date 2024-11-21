from nicegui import ui
from api.road_retreiver import RoadRetreiver
from api.utils import open_finder_macos
from ui.report_form import ReportFormGUI
from ui.road_gui import RoadGUI
from ui.last_reports_list import last_reports_list
import subprocess
import os


def main_page():
    with ui.header():
        ui.label("Дороги")
        ui.button(icon="folder", on_click=lambda: open_finder_macos())
    with ui.row().style("width: 100%"):
        with ui.column().style("width: 75rem"):
            RoadGUI()
        with ui.column().style("width: 20rem"):
            with ui.grid(rows=2):
                ReportFormGUI()
                last_reports_list()
