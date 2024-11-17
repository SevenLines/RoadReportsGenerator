from nicegui import ui
import os
from api.utils import open_finder_macos


def last_reports_list():
    with ui.card():
        ui.label("Последние отчеты").style("font-weight: bold;")
        with ui.grid(columns=4): 
            for f in os.listdir("output"):
                ui.label(f)
                ui.label("")
                ui.label("")
                ui.button(icon="folder", on_click=lambda: open_finder_macos(f)).style(
                    "width: 3rem; height: 3rem;"
                )
