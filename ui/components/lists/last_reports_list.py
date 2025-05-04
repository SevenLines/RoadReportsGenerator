from nicegui import ui
import os
from api.utils import open_finder_macos



class LastReportsListComponent:
    def __init__(self):
        self.contaner = ui.card().style("height: 100%")
        self.render()

    def render(self):
        with self.container:
            ui.label("Последние отчеты").style("font-weight: bold;")
            with ui.grid(columns=4):
                for f in os.listdir("output")[::-1][:3]:
                    ui.label(f)
                    ui.label("")
                    ui.label("")
                    ui.button(icon="folder", on_click=lambda: open_finder_macos(f)).style(
                        "width: 3rem; height: 3rem;"
                    )
