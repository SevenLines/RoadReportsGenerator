from nicegui import ui

def sidebar(
    tabs: dict[str, str],
    panels: dict[str, callable],

):
    tab_dict={}
    with ui.splitter(value=6).classes('w-full h-full') as splitter:
        with splitter.before:
            with ui.tabs().props('vertical').classes('w-full') as ui_tabs:
                for tab_label, tab_icon in tabs.items():
                    tab_dict[tab_label] = ui.tab(tab_label, icon=tab_icon)
                print(tab_dict)
        with splitter.after:
            with ui.tab_panels(ui_tabs, value=list(tabs.values())[0]) \
                    .props('vertical').classes('w-full h-full'):
                for tab_label in tabs.keys():
                    with ui.tab_panel(tab_dict[tab_label]):
                        ui.label(tab_label).classes('text-h4')
                        panels[tab_label]()
                
        ui_tabs.set_value('Генерация')