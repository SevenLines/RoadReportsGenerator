from nicegui import ui

from api.managers.sqlite import SavedFileTemplateManager
from ui.components.base import BaseComponent
from api.report_generator import ReportGenerator
from api.managers.road_factory import RoadManagerFactory
from ui.components.template_settings import TemplateSettingsForm
from api.contexts.data_context import AppContext
from ui.dialogs.progress_bar import ReportProgressBar
import os


class ReportFormGUI(BaseComponent):
    manager = SavedFileTemplateManager()

    def __init__(self):
        self.report_generator = ReportGenerator()
        self.form = self.report_form()

    def report_form(self):
        with ui.card().style("height: 100%; width: 100%"):
            ui.label("Отчет").style("font-weight: bold;")
            self.template_choise()

            ui.button(
                "Сформировать",
                on_click=lambda: self.start_reporting(),
            )
            self.progress_bar = ReportProgressBar()
            # self.progress_bar.hide()x
        with ui.card().style("height: 100%; width: 100%"):
            self.settings = TemplateSettingsForm()

    def template_choise(self):
        templates = self.manager.get_objects()
        options = {t.id: t.path for t in templates}
        self.template_select = ui.select(
            options=options,
            label="Выбор Шаблона",
            with_input=True,
        ).props("rounded outlined dense")
        self.template_settings = None
        # ui.button(
        #     "Настроить переменные", on_click=lambda: self.show_template_settings()
        # )
        self.template_select.on_value_change(self.select_template)

    # def show_template_settings(self):
    #     if self.template_settings:
    #         self.template_settings.clear()
    #     self.template_settings = TemplateSettingsForm()

    def select_template(self, change):
        AppContext.context["selected_template"] = change.value
        print(change.value)
        self.settings.update()

    def start_reporting(self):
        if len(AppContext.context["selected_ids"]) == 0:
            ui.notify("Выберите документы для формирования отчета")
        else:
            AppContext.context["stop_thread"] = False
            self.progress_bar.show()
            self.report_generator.start_multy_thread(
                AppContext.context["selected_ids"]
            )
