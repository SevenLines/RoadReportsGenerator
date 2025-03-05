from docxtpl import DocxTemplate
from nicegui import ui
from api.context import AppContextManager
import os


class TemplateSettingsForm:
    def __init__(self):
        self.get_variables()
        with ui.dialog() as self.dialog, ui.card() as form:
            ui.label("Настройка переменных")
            with ui.column():
                for k, var in AppContextManager.context["form_variables"].items():
                    with ui.row().style("width:100%"):
                        ui.input(
                            label=k,
                            value=var,
                            on_change=lambda v: self.on_value_changed(k, v),
                        )

            ui.button("Сохранить", on_click=self.hide)

    def get_variables(self):
        if AppContextManager.context["selected_template"]:
            template = DocxTemplate(
                os.path.join(
                    "templates", AppContextManager.context["selected_template"]
                )
            )
            vars = template.get_undeclared_template_variables()
            AppContextManager.get_form_context(vars)

    def on_value_changed(self, k, v):
        try:
            AppContextManager.context["form_variables"][k] = int(v.value)
        except ValueError:
            AppContextManager.context["form_variables"][k] = v.value

    def hide(self):
        self.dialog.close()

    def show(self):
        self.dialog.open()
