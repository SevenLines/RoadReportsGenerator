from nicegui import ui
from api.road_retreiver import RoadRetreiver
from ui.report_form import ReportFormGUI
from ui.road_gui import RoadGUI



def main_page():

    with ui.header():
        ui.label("Дороги")
    with ui.row():
        with ui.column():
            RoadGUI()
        ReportFormGUI()
        

    ui.run(native=True)
