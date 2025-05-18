from nicegui import ui

from api.managers.sqlite import DBConnectionManager
from ui.components.base import BaseComponent
class DBConnectionFormComponent(BaseComponent):
    manager = DBConnectionManager()
    context_key = "connection_history"

    def get_container(self):
        return ui.card().style("width: 30rem")
    
    
    @ui.refreshable
    def render(self):
        with self.container:
            with ui.grid(columns=2):
                ui.label("host")
                host = ui.input(placeholder="localhost").props("rounded outlined dense")

                ui.label("db_name")
                db_name = ui.input(placeholder="msql").props("rounded outlined dense")


                ui.label("user")
                user = ui.input(placeholder="sa").props("rounded outlined dense")


                ui.label("password")
                password = ui.input(placeholder="superstrongpassword").props("rounded outlined dense")

            ui.button("Сохранить", on_click=lambda: self.save_connection(
                host=host.value,
                user=user.value,
                db_name=db_name.value,
                password=password.value
                ))

        
    def save_connection(
        self,
        host:str,
        user:str,
        db_name:str,
        password:str,
        ):
        self.manager.add_object({
            "host":host,
            "user":user,
            "db_name":db_name,
            "password":password
        })
        

