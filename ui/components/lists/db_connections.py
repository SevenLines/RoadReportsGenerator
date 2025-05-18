from nicegui import ui

from api.managers.sqlite import SavedFileConnectionManager, DBConnectionManager
from api.contexts.state import StateContext
from ui.components.base import BaseComponent

class SavedConnectionComponent(BaseComponent):

    context_key = "connection_history"
    manager = DBConnectionManager()

    def get_container(self):
        return ui.card().style("width:30rem").props('dense separator')

    @ui.refreshable
    def render(self):
        db_connections = self.manager.get_objects()

        db_options = {}

        for c in db_connections:
            db_options[c.id]=f"{c.user}-{c.db_name}"

        with self.container:
            ui.button(
                    "Сбросить",
                    on_click=lambda :self.update()
                )

            ui.label("БД")

            ui.select(
                options=db_options,
                on_change=lambda e: (StateContext.set_value(
                    "current_connection",{"db":
                    self.manager.get_object(e.value)
                    }
                    )
                )
            ).style("width:20rem").props("rounded outlined dense")



