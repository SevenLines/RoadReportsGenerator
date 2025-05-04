from nicegui import ui

from api.managers.implementations import TemplateManager
from ui.components.lists.saved_templates import SavedTemplatesListComponent
from ui.components.forms.template_meta_data import TemplateVariablesForm


def template_view():
    manager = TemplateManager()

    with ui.row().classes("col-span-full"):
        with ui.column().classes('col-span-2'):
            ui.label("Добавить шаблон")
            ui.upload(
                label="Загрузить файл",
                on_upload=lambda file: (
                    ui.notify(f"{file.name}"),
                    manager.add_object(file),
                    template_list.update()
                    )
                ).style("width: 30rem")

        with ui.column().classes('col-span-2'):
            ui.label("Сохраненные шаблоны")  
            template_list = SavedTemplatesListComponent()

        with ui.column().classes('col-span-2'):
            ui.label("Установка переменных генерации")
            template_variables_form = TemplateVariablesForm()

