import os

from docxtpl import DocxTemplate

from db import RoadsDB
from models import Road, High, Way


class BaseGenerator(object):
    template = ""
    tables_generators = {}

    def generate(self, road_id):
        doc_template = DocxTemplate(os.path.join("templates", self.template))
        doc = doc_template.get_docx()

        tables_to_fill = []

        db = RoadsDB()
        with db.session() as s:
            road = s.query(Road).filter(Road.id == road_id).first()
            road_length = road.get_length(s)[1]
            high = s.query(High).join(Way, Way.id == High.way_id) \
                .filter(Way.road_id == road.id).first()

        for table in doc.tables:
            key = table.rows[0].cells[0].text[1:-1].strip()
            generator_class = self.tables_generators.get(key)
            if generator_class:
                tables_to_fill.append({
                    'table': table,
                    'generator': generator_class,
                })

        for table_info in tables_to_fill:
            table_info['generator'](high.id, db).fill(table_info['table'], doc)

        context = {
            'road_title': road.Name,
            'road_length': road_length,
        }
        doc_template.render(context)
        doc_template.save("test.docx")