from pprint import pprint


from db import RoadsDB
from generators.tech_passport_generator import TechPassportGenerator

from table_generators.generators import SignTableGenerator

generator = TechPassportGenerator()
generator.generate(525770)

