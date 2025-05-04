from nicegui import ui

from api.managers.implementations import TemplateManager
from api.contexts.state import StateContext
from ui.components.base import BaseComponent

class SavedTemplatesListComponent(BaseComponent):

    manager = TemplateManager()
    context_key = "current_template"


    def get_container(self):
        return ui.list().props('dense separator')

    @ui.refreshable
    def render(self):
        options = self.manager.get_objects()
        with self.container:
            ui.radio(
                options=options,
                on_change=lambda e:StateContext.set_value(self.context_key,e.value)
                )
    
    def update(self, *_):
        pass
    # def update(self, *_):

    #     self.render.refresh()

