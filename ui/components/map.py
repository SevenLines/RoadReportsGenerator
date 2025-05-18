from statistics import mean
from nicegui import ui
from api.managers.road_factory import RoadManagerFactory
from api.contexts.data_context import AppContext
from api.db import RoadsDB
from models import Road


class RoadMap:
    def __init__(self):
        self.label = ui.label("Карта:").style("font-weight: bold; height: 1rem")
        self.road_label = ui.label("").style("font-weight: bold; height: 0.5rem")

        self.map = ui.leaflet(
            center=AppContext.context["default_center"], zoom=15
        ).style("height: 40rem; width: 40rem")
        ui.add_css(
            """
            .leaflet-control-attribution {
                display: none !important;
            }
        """
        )

    def change_map_center(self, id):
        if id is None:
            self.map.set_center(AppContext.context["default_center"])
        else:
            with RoadManagerFactory().db().session() as s:
                road = s.query(Road).filter(Road.id == id).first()
                self.road_label.set_text(road.Name)
                axe = road.get_main_axe_coordinates(s)
                lng = mean(i["lng"] for i in axe)
                lat = mean(i["lat"] for i in axe)
                LAT_DIFFERENCE = 0.00175
                LNG_DIFFERENCE = 0.0085
                self.map.set_center([lat - LAT_DIFFERENCE, lng - LNG_DIFFERENCE])
                options = {"color": "red", "weight": 1}
                axe = [
                    {"lat": i["lat"] - LAT_DIFFERENCE, "lng": i["lng"] - LNG_DIFFERENCE}
                    for i in axe
                ]
                self.map.generic_layer(name="polyline", args=[axe, options])
                self.map.update()
