from nicegui import ui
from api.utils import choose_file
from ui.components.base import BaseComponent
from api.managers.sqlite import SavedFileConnectionManager, SavedFileTemplateManager


class SaveFileForm(BaseComponent):


    def get_container(self):
        return ui.card().style("width: 30rem")
    
    def update_container(self):
        self.str_container = choose_file()

    def render(self):
        with self.container:
            self.str_container = ""
            file_label = ui.label("Файл не выбран")
            with ui.row():
                ui.button(
                    "Выбрать файл",
                    on_click=lambda : (
                        self.update_container(),
                        file_label.set_text(
                        "Выбран файл - " + 
                        self.str_container
                        )
                ))
                ui.button(
                    "Сохранить",
                    on_click=lambda e:self.manager.add_object({
                        "path": self.str_container, 
                        "is_connection": self.is_connection
                    })
                )

class SaveConnectionFileForm(SaveFileForm):
    manager = SavedFileConnectionManager()
    context_key = "connection_history_access"
    is_connection = True

class SaveTemplateFileForm(SaveFileForm):
    manager = SavedFileTemplateManager()
    context_key = "template_list"
    is_connection = False