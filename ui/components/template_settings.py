from docxtpl import DocxTemplate
from nicegui import ui
from api.contexts.data_context import AppContext
import os


class TemplateSettingsForm:
    def __init__(self):
        self.get_variables()
        ui.label("Настройка переменных")
        self.col = ui.column()
            

    def render_variable_list(self):
        self.col.clear()
        with self.col:
            for k, var in AppContext.context["form_variables"].items():
                print(k,var)
                with ui.row().style("width:100%"):
                    ui.input(
                        label=k,
                        value=var,
                        on_change=lambda v: self.on_value_changed(k, v),
                    )

    def update(self):
        self.get_variables()
        self.render_variable_list()

    def get_variables(self):
        if AppContext.context["selected_template"]:
            template = DocxTemplate(
                os.path.join(
                    "templates", AppContext.context["selected_template"]
                )
            )
            vars = template.get_undeclared_template_variables()
            AppContext.get_form_context(vars)

    def on_value_changed(self, k, v):
        try:
            AppContext.context["form_variables"][k] = int(v.value)
        except ValueError:
            AppContext.context["form_variables"][k] = v.value
