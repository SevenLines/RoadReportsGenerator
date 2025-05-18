from nicegui import ui

from api.managers.sqlite import SavedFileTemplateManager
from ui.components.lists.saved_templates import SavedTemplatesListComponent
from ui.components.forms.template_meta_data import TemplateVariablesForm
from ui.components.forms.saved_file_form import SaveTemplateFileForm

def template_view():
    manager = SavedFileTemplateManager()

    with ui.row().classes("col-span-full"):
        with ui.column().classes('col-span-2'):
            ui.label("Добавить шаблон")
            SaveTemplateFileForm()

        with ui.column().classes('col-span-2'):
            ui.label("Сохраненные шаблоны")  
            template_list = SavedTemplatesListComponent()

        with ui.column().classes('col-span-2'):
            ui.label("Установка переменных генерации")
            template_variables_form = TemplateVariablesForm()

