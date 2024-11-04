from db import RoadsDB
from generators.tech_passport_generator_20241019 import TechPassportGenerator20241019
from models import Road

generator = TechPassportGenerator20241019()


with RoadsDB().session() as s:
    roads = s.query(Road).filter(
        Road.id.in_([1149658, 1149629, 1149599])
        # Road.id.in_([1149658])
        # Road.Name.startswith("Иволгинское МО - ")
    )

    for r in roads:
        # data = generator.test_generator(r.id, CoverTypeTableGenerator)
        # print(data)
        generator.generate(r.id, with_image=True)
