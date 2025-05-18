# example.py - Пример использования компонента SimpleSidebar
from nicegui import ui
from test_ui.sidebar import SimpleSidebar
from test_ui.components.db_settings import create_db_settings
from test_ui.components.template_settings import create_template_gui
def main_screen():
    # Добавляем стили для анимации
    ui.add_head_html("""
    <style>
    .transition-all {
        transition: all 0.3s ease-in-out;
    }
    .duration-300 {
        transition-duration: 300ms;
    }
    </style>
    """)
    
    # Создаем контейнер с сеткой для размещения сайдбара и контента
    with ui.row().classes('h-screen w-full gap-0'):
        # Создаем сайдбар
        sidebar = SimpleSidebar()
        sidebar_container = sidebar.create()
        
        # Добавляем кнопки в сайдбар
        sidebar.add_button('storage', 'settings', 'БД')
        sidebar.add_button('template', 'document', 'Шаблон')


        # Регистрируем компоненты для отображения в сайдбаре
        sidebar.register_component('storage', create_db_settings, 'БД')
        sidebar.register_component('template',create_template_gui,"Шаблон")

        
        # Основной контент
        with ui.column().classes('flex-grow p-4'):
            ui.label('Основной контент').classes('text-2xl font-bold mb-4')
            ui.label('Нажмите на кнопку в сайдбаре, чтобы увидеть соответствующий компонент')

# Функции для создания компонентов





