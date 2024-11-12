from nicegui import ui

from api.report_generator import ReportGenerator
from api.road_retreiver import RoadRetreiver
from ui.context import context

class ReportFormGUI:

    def __init__(self):
        self.report_generator = ReportGenerator()
        self.form = self.report_form()

    def report_form(self):
        with ui.card():
            ui.label("Отчет").style("font-weight: bold;")
            ui.button(
                "Сформировать",
                on_click=lambda: self.report_generator.report(context['selected_id'])  
            )
    
    