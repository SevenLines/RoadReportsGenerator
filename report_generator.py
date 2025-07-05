from tqdm import tqdm

from db import RoadsDB
from generators.tech_passport_generator import TechPassportGenerator
from generators.tech_passport_generator_20241019 import TechPassportGenerator20241019
from models import Road

generator = TechPassportGenerator()


with RoadsDB().session() as s:
    roads = list(s.query(Road).filter(
        # Road.id.in_([
        #     1150453,
        #     1150391,
        #     1150332,
        #     1150269,
        #     1150209,
        #     1150148,
        #     1150083,
        # ])
        Road.id.in_([2403296, 2403285])
        # Road.id >= 1832,
        # Road.Name.startswith("Хомутово")
    ))

    for r in tqdm(roads):
        # data = generator.test_generator(r.id, CoverTypeTableGenerator)
        # print(data)
        generator.generate(r.id, with_image=False)
