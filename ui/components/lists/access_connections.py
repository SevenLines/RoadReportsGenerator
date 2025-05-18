from nicegui import ui

from api.managers.sqlite import SavedFileConnectionManager, DBConnectionManager
from api.contexts.state import StateContext
from ui.components.base import BaseComponent

class AccessSavedConnectionComponent(BaseComponent):

    context_key = "connection_history"
    manager = SavedFileConnectionManager()

    def get_container(self):
        return ui.card().style("width:30rem").props('dense separator')


    @ui.refreshable
    def render(self):
        access_connections = self.manager.get_objects()
        access_options = {}

        for c in access_connections:
            access_options[c.id]=f"{c.path}"

        with self.container:
            ui.button(
                    "Сбросить",
                    on_click=lambda :self.update()
                )
           
            ui.label("Access")
            ui.select(
                options=access_options,
                on_change=lambda e: StateContext.set_value(
                    "current_connection",{"access":
                    self.manager.get_object(e.value)
                    })
            ).style("width:20rem").props("rounded outlined dense")


