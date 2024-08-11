from pprint import pprint


from db import RoadsDB

from table_generators.generators import SignTableGenerator

db = RoadsDB()
generator = SignTableGenerator(366311, db)
data = generator.prepare_data()

pprint(data)
