# sidebar.py - Простой компонент сайдбара с возможностью расширения
from nicegui import ui

class SimpleSidebar:
    def __init__(self):
        self.container = None
        self.expanded = False
        self.content_container = None
        self.active_component = None
        self.components = {}  # Словарь для хранения компонентов
        self.buttons = {}     # Словарь для хранения кнопок
        self.active_button_id = None
    
    def create(self, default_width="16", expanded_width="64"):
        """Создание компонента сайдбара
        
        Args:
            default_width: ширина свернутого сайдбара (в rem или px)
            expanded_width: ширина развернутого сайдбара (в rem или px)
        """
        with ui.column().classes(f'bg-blue-800 text-white h-screen shadow-lg transition-all duration-300 w-{default_width}') as container:
            self.container = container
            self.default_width = default_width
            self.expanded_width = expanded_width
            
            # Верхняя часть сайдбара (всегда видна)
            with ui.column().classes('w-full'):
                # # Логотип/заголовок
                # with ui.element('div').classes('p-4 flex justify-center items-center'):
                #     ui.icon('apps', size='lg').classes('text-white')
                
                # ui.separator()
                
                # Контейнер для кнопок
                with ui.column().classes('w-full gap-1 p-2 items-center') as self.buttons_container:
                    pass
                
                ui.separator()
                
                # Кнопка для сворачивания/разворачивания сайдбара
                with ui.element('div').classes('p-2 flex justify-center'):
                    toggle_btn = ui.button(icon='menu', on_click=self.toggle_sidebar)\
                        .props('flat round')
            
            # Контейнер для содержимого развернутого сайдбара
            with ui.column().classes('w-full p-2').style('display: none') as content:
                self.content_container = content
                
                # Заголовок (будет меняться в зависимости от выбранной кнопки)
                self.content_title = ui.label('').classes('text-lg font-bold mb-2')
                
                # Контейнер для динамического содержимого
                with ui.column().classes('w-full') as self.dynamic_content:
                    pass
        
        return container
    
    def add_button(self, button_id, icon, label=None, on_click=None):
        """Добавление кнопки в сайдбар
        
        Args:
            button_id: уникальный идентификатор кнопки
            icon: иконка для кнопки (из Material Icons)
            label: текст кнопки (отображается только в развернутом состоянии)
            on_click: функция, вызываемая при нажатии на кнопку (опционально)
        """
        with self.buttons_container:
            # Создаем кнопку только с иконкой для компактного режима
            button = ui.button(icon=icon, on_click=lambda: self.handle_button_click(button_id, on_click))\
                .props('flat round').classes('mb-2 w-full')
            
            # Сохраняем кнопку в словаре
            self.buttons[button_id] = {
                'button': button,
                'icon': icon,
                'label': label or button_id.capitalize(),
                'on_click': on_click
            }
        
        return button
    
    def register_component(self, component_id, component_creator_func, title=None):
        """Регистрация компонента для отображения в развернутом сайдбаре
        
        Args:
            component_id: уникальный идентификатор компонента
            component_creator_func: функция, создающая компонент
            title: заголовок, отображаемый при активации компонента
        """
        self.components[component_id] = {
            'creator': component_creator_func,
            'instance': None,
            'title': title or component_id.capitalize()
        }
    
    def toggle_sidebar(self):
        """Переключение состояния сайдбара (свернут/развернут)"""
        self.expanded = not self.expanded
        
        if self.expanded:
            self.container.classes(f'w-{self.expanded_width}', remove=f'w-{self.default_width}')
            self.content_container.style('display: block')
            
            # Если есть активный компонент, отображаем его
            if self.active_button_id and self.active_button_id in self.components:
                self.show_component(self.active_button_id)
        else:
            self.container.classes(f'w-{self.default_width}', remove=f'w-{self.expanded_width}')
            self.content_container.style('display: none')
            
            # Скрываем все компоненты
            self.hide_all_components()
    
    def handle_button_click(self, button_id, custom_on_click=None):
        """Обработка нажатия на кнопку в сайдбаре"""
        # Если сайдбар свернут, разворачиваем его
        if not self.expanded:
            self.toggle_sidebar()
        
        # Обновляем активную кнопку
        self.active_button_id = button_id
        
        # Если для кнопки зарегистрирован компонент, отображаем его
        if button_id in self.components:
            self.show_component(button_id)
        
        # Если передан пользовательский обработчик, вызываем его
        if custom_on_click:
            custom_on_click()
    
    def show_component(self, component_id):
        """Отображение компонента в развернутом сайдбаре"""
        # Скрываем все компоненты
        self.hide_all_components()
        
        # Получаем информацию о компоненте
        component_info = self.components.get(component_id)
        if not component_info:
            return
        
        # Устанавливаем заголовок
        self.content_title.set_text(component_info['title'])
        
        # Если компонент еще не создан, создаем его
        if not component_info['instance']:
            # Очищаем контейнер для динамического содержимого
            self.dynamic_content.clear()
            
            # Создаем компонент
            with self.dynamic_content:
                component_info['instance'] = component_info['creator']()
        
        # Отображаем компонент
        # if hasattr(component_info['instance'], 'visible'):
        #     component_info['instance'].visible = True
        # elif hasattr(component_info['instance'], 'style'):
        #     component_info['instance'].style('display: block')
    
    def hide_all_components(self):
        """Скрытие всех компонентов"""
        for component_id, component_info in self.components.items():
            if component_info['instance']:
                if hasattr(component_info['instance'], 'visible'):
                    component_info['instance'].visible = False
                elif hasattr(component_info['instance'], 'style'):
                    component_info['instance'].style('display: none')