from db import RoadsDB
from generators.tech_passport_generator import TechPassportGenerator
from models import Road

generator = TechPassportGenerator()

with RoadsDB().session() as s:
    roads = s.query(Road).filter(Road.Name.startswith("Хомутово - Н Каландаришвили"))

    for r in roads:
        print(r.Name)
        generator.generate(r.id, with_image=True)

