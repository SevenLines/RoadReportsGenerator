from db import RoadsDB
from generators.tech_passport_generator_20241019 import TechPassportGenerator20241019
from generators.tech_passport_generator import TechPassportGenerator
from models import Road
from threading import Thread
from api.context import AppContextManager


class TemplateChoser:
    choises = {
        "tech_passport_generator.docx": TechPassportGenerator,
        "tech_passport_generator2.docx": TechPassportGenerator20241019,
    }


class ReportGenerator:
    choser = TemplateChoser

    def receive_data(self, ids: list[int]):
        with RoadsDB().session() as s:
            self.roads = s.query(Road).filter(
                Road.id.in_(ids)
                # Road.id.in_([1149658])
                # Road.Name.startswith("Иволгинское МО - ")
            )

    def report(self):
        generator = self.choser.choises[
            AppContextManager.context["selected_template"]
        ]()
        for i, r in enumerate(self.roads):
            if AppContextManager.context["stop_thread"]:
                break
            AppContextManager.context["current_road_name"] = r.Name
            AppContextManager.context["current_road"] = (i + 1) / self.roads.count()
            # data = generator.test_generator(r.id, CoverTypeTableGenerator)
            # print(data)
            print(r.id)
            generator.generate(r.id, with_image=True)
        # Завершаем поток при завершении генерации
        print("done")
        AppContextManager.context["stop_thread"] = True

    def start_multy_thread(self, ids: list[int]):
        self.receive_data(ids)
        thread = Thread(target=self.report)
        thread.start()
