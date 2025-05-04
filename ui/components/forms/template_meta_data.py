from nicegui import ui
from api.managers.implementations import TemplateVariablesManager
from api.contexts.state import StateContext
from ui.components.base import BaseComponent

class TemplateVariablesForm(BaseComponent):

    context_key = "current_template"
    manager = TemplateVariablesManager()

    def get_container(self):
        return ui.card().style("width:30rem")


    @ui.refreshable
    def render(self):
        template_variables = self.manager.get_object(
            StateContext.get_value("current_template")
            ) or {}
        with self.container:
            if len(template_variables) == 0:
                ui.label("Переменные отсутсвуют")
            else:
                self.inputs = {}
                btn = ui.button("Сохранить", on_click=self.save).props("color=primary")
                for k,v in template_variables.items():
                    (ui.label(f"Заполненное значение {v}")
                        if v is not None 
                        else ui.label("Значение не заполнено"))
                    self.inputs[k] = ui.input(
                        label=k,
                        placeholder=v,
                        on_change=lambda v: ui.notify(v.value),
                        ).props("rounded outlined dense")


    def save(self):
        data = {var: input_.value for var, input_ in self.inputs.items()}
        self.manager.save_variables(StateContext.get_value("current_template"), data)
        ui.notify("Переменные успешно сохранены!")
