import os

from docxtpl import DocxTemplate

from db import RoadsDB


class BaseGenerator(object):
    template = ""
    tables_generators = {}

    def generate(self, high_id):
        doc_template = DocxTemplate(os.path.join("templates", self.template))
        doc = doc_template.get_docx()

        tables_to_fill = []

        db = RoadsDB()

        for table in doc.tables:
            key = table.rows[0].cells[0].text[1:-1].strip()
            generator_class = self.tables_generators.get(key)
            if generator_class:
                tables_to_fill.append({
                    'table': table,
                    'generator': generator_class,
                })

        for table_info in tables_to_fill:
            table_info['generator'](high_id, db).fill(table_info['table'], doc)

        context = {
        }
        doc_template.render(context)
        doc_template.save("test.docx")