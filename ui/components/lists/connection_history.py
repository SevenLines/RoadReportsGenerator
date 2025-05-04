from nicegui import ui

from api.managers.implementations import ConnectionManager
from api.contexts.state import StateContext
from ui.components.base import BaseComponent

class SavedConnectionComponent(BaseComponent):

    context_key = "connection_history"
    manager = ConnectionManager()


    def get_container(self):
        return ui.list().props('dense separator')

    @ui.refreshable
    def render(self):
        connections = self.manager.get_objects()
        options = {}
        for c in connections:
            options[c.id]=f"{c.user}-{c.db_name}"

        with self.container:
            ui.radio(
                options=options,
                on_change=lambda e: StateContext.set_value(
                    "current_connection",
                    self.manager.get_object(e.value)
                    )
            )


