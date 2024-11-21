from db import RoadsDB
from generators.tech_passport_generator_20241019 import TechPassportGenerator20241019
from models import Road
from threading import Thread
from ui.context import context
class ReportGenerator:
    generator = TechPassportGenerator20241019()

    def receive_data(self, ids: list[int]):
        with RoadsDB().session() as s:
            self.roads = s.query(Road).filter(
                Road.id.in_(ids)
                # Road.id.in_([1149658])
                # Road.Name.startswith("Иволгинское МО - ")
            )

    def report(self):
        for i, r in enumerate(self.roads):
            if context['stop_thread']:
                break
            context['current_road_name'] = r.Name
            context['current_road'] = (i + 1)/self.roads.count()
            # data = generator.test_generator(r.id, CoverTypeTableGenerator)
            # print(data)
            self.generator.generate(r.id, with_image=True)

    def start_multy_thread(self, ids: list[int]):
        self.receive_data(ids)
        thread = Thread(target=self.report)
        thread.start()