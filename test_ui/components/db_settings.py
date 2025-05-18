from nicegui import ui

def create_db_settings():
    with ui.card().classes('w-full'):
        ui.label('Подключение к БД').style("color:black").classes('text-lg font-bold mb-2')
        ui.select(options=[
            "test","test","test"
        ],value="test")
        with ui.column().classes('w-full gap-2'):
            host_input = ui.input(label="Введите хост",placeholder="host")
            port_input = ui.input(label="Введите порт",placeholder="host")
            login_input = ui.input(label="Введите Логин",placeholder="sa")
            password_input = ui.input(label="Введите пароль",placeholder="password", password=True)

            
            
            # Кнопка сохранения настроек
            ui.button('Сохранить настройки', on_click=lambda: ui.notify('Настройки сохранены'))\
                .classes('w-full mt-2').props('color=primary')
    
    return ui.element('div')  # Возвращаем элемент-контейнер