from db import RoadsDB
from generators.tech_passport_generator_20241019 import TechPassportGenerator20241019
from models import Road


class ReportGenerator:
    generator = TechPassportGenerator20241019()

    def report(self, ids: list[int]):
        with RoadsDB().session() as s:
            roads = s.query(Road).filter(
                Road.id.in_(ids)
                # Road.id.in_([1149658])
                # Road.Name.startswith("Иволгинское МО - ")
            )

            for r in roads:

                # data = generator.test_generator(r.id, CoverTypeTableGenerator)
                # print(data)
                self.generator.generate(r.id, with_image=True)
