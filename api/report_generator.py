from api.managers.road_factory import RoadManagerFactory
from generators.base_generator import BaseGenerator
from api.managers.sqlite import SavedFileTemplateManager
from api.db import RoadsDB
from generators.tech_passport_generator_20241019 import TechPassportGenerator20241019
from generators.tech_passport_generator import TechPassportGenerator
from models import Road
from threading import Thread
from api.contexts.data_context import AppContext



class ReportGenerator:
    manager = SavedFileTemplateManager()

    def receive_data(self, ids: list[int]):
        with RoadManagerFactory().db().session() as s:
            self.roads = s.query(Road).filter(
                Road.id.in_(ids)
            )

    def report(self):
        generator = BaseGenerator() 
        template = self.manager.get_object(
            AppContext.context["selected_template"]
        )
        for i, r in enumerate(self.roads):
            if AppContext.context["stop_thread"]:
                break
            AppContext.context["current_road_name"] = r.Name
            AppContext.context["current_road"] = (i + 1) / self.roads.count()

            generator.generate(r.id,template_path=template.path, with_image=True)
        # Завершаем поток при завершении генерации
        # print("done")
        AppContext.context["stop_thread"] = True

    def start_multy_thread(self, ids: list[int]):
        self.receive_data(ids)
        thread = Thread(target=self.report)
        thread.start()
