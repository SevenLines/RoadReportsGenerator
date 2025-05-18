from nicegui import ui

def create_template_gui():
     with ui.card().classes('w-full'):
        ui.label('Выбор шаблона').style("color:black").classes('text-lg font-bold mb-2')
        with ui.column().classes('w-full gap-2'):
            ui.select(options=[
                "Шаблон1","Шаблон2","Шаблон3"
            ],value="Шаблон1").classes('w-full gap-2')
            file_input = ui.upload().classes('w-full gap-2')
             # Кнопка сохранения настроек
            ui.button('Сохранить настройки', on_click=lambda: ui.notify('Настройки сохранены'))\
                .classes('w-full mt-2').props('color=primary')