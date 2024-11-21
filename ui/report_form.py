from nicegui import ui

from api.report_generator import ReportGenerator
from api.road_retreiver import RoadRetreiver
from ui.context import context
from ui.progress_bar import ReportProgressBar


class ReportFormGUI:

    def __init__(self):
        self.report_generator = ReportGenerator()
        self.form = self.report_form()

    def report_form(self):        
        with ui.card():
            ui.label("Отчет").style("font-weight: bold;")
            ui.button(
                "Сформировать",
                on_click=lambda: self.start_reporting(),
            )
            self.progress_bar = ReportProgressBar()
            # self.progress_bar.hide()x

    def start_reporting(self):
        if len(context["selected_ids"]) == 0:
            ui.notify("Выберите документы для формирования отчета")
        else:
            context["stop_thread"] = False
            self.progress_bar.show()
            self.report_generator.start_multy_thread(context["selected_ids"])
