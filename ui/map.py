from statistics import mean
from nicegui import ui
from ui.context import context
from db import RoadsDB
from models import Road

class RoadMap:
    def __init__(self):
        ui.label("Карта").style("font-weight: bold;")
        self.map = ui.leaflet(center=[55.751244, 37.618423], zoom=12).style(
            "height: 40rem; width: 40rem"
        )
        ui.add_css(
            """
            .leaflet-control-attribution {
                display: none !important;
            }
        """
        )
    
    def change_map_center(self, id):
        if id is None:
            self.map.set_center(context["default_center"])
        else:
            with RoadsDB().session() as s:
                road = s.query(Road).filter(Road.id == id).first()
                axe = road.get_main_axe_coordinates(s)
                lng = mean(i['lng'] for i in axe)
                lat = mean(i['lat'] for i in axe)
                self.map.set_center([lat, lng])
                print((lng,lat))