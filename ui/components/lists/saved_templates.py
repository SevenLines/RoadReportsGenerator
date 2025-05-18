from nicegui import ui

from api.managers.sqlite import SavedFileTemplateManager
from api.contexts.state import StateContext
from ui.components.base import BaseComponent

class SavedTemplatesListComponent(BaseComponent):

    manager = SavedFileTemplateManager()
    context_key = "template_list"


    def get_container(self):
        return ui.card().style("width:30rem")

    @ui.refreshable
    def render(self):
        objs = self.manager.get_objects()
        options = {}
        for obj in objs:
            options[obj.id] = obj.path
        with self.container:
            ui.select(
                options=options,
                on_change=lambda e:(print(e.value), StateContext.set_value("current_template",e.value))
                ).style("width:20rem").props("rounded outlined dense")
    

