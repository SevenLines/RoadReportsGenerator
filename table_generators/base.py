import json
from collections import namedtuple
from dataclasses import dataclass

from docx.document import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from sqlalchemy import text, bindparam

from models import Attribute

POSITION_LEFT = -1
POSITION_RIGHT = 1
POSITION_BOTH = 0


@dataclass
class DbRow:
    id: int
    name: str
    type: int
    begin: int
    begin_km: int
    begin_m: int
    end: int
    end_km: int
    end_m: int
    position: str
    is_left: bool
    is_right: bool
    is_cross: bool
    format: int
    params: dict

class TableGeneratorBase(object):
    condition = ""
    title = ""

    def __init__(self, high_id, db):
        self.db = db
        self.high_id = high_id

    @staticmethod
    def remove_row(table: Table, row):
        tbl = table._tbl
        tr = row._tr
        tbl.remove(tr)

    def _get_raw_data(self):
        with self.db.session() as s:
            items = list(s.execute(text(f"""
            EXEC ExelReport {self.high_id}, 1, {self.condition}, 0.000000, 10000000, 1
            """)))
            query = text(f"""
            select ID_Attribute, Image_Points, Image_Counts from Attribute where (ID_Attribute in :ids)            
            """)

            query = query.bindparams(bindparam('ids', expanding=True))
            attributes_info = {i.ID_Attribute: i for i in s.execute(query, {
                "ids": [i.ID_Attribute for i in items]
            })}
        result = []

        with self.db.session() as s:
            for item in items:
                points = Attribute.get_points(attributes_info[item.ID_Attribute].Image_Points,
                                              attributes_info[item.ID_Attribute].Image_Counts)

                max_p = max([p.a for p in points])
                min_p = min([p.a for p in points])

                if max_p * min_p < 0:
                    position = 'пересекает'
                elif max_p > 0:
                    position = 'справа'
                else:
                    position = 'слева'

                item_data = DbRow(**{
                    "id": item.ID_Attribute,
                    "name": item._asdict()['Название атрибута'],
                    "type": item.ID_Type_Attr,
                    "begin": item.Начало,
                    "begin_km": item.Начало // 1000,
                    "begin_m": item.Начало % 1000,
                    "end": item.Конец,
                    "end_km": item.Конец // 1000,
                    "end_m": item.Конец % 1000,
                    "position": position,
                    "is_left": position == 'слева',
                    "is_right": position == 'справа',
                    "is_cross": position == 'пересекает',
                    "format": item.ID_Format,
                    "params": {}
                })

                params = s.execute(text(f"""
                SELECT Params.ID_Param, Types_Description.Param_Name, Params.ValueParam, Params.Suffix FROM Params INNER JOIN Types_Description ON Params.ID_Param = Types_Description.ID_Param WHERE (Params.ID_Attribute = {item.ID_Attribute})  and Params.ID_RegDate=dbo.GetIndexDate(1,Params.ID_Param,Params.ID_Attribute) order by Params.ID_Param
                """))
                for p in params:
                    item_data.params[p.Param_Name] = p.ValueParam

                result.append(item_data)
        return result

    def fill(self, table: Table, doc: Document):
        data = self._get_raw_data()

        if not data:
            p = table._tbl.getnext()
            paragraph = Paragraph(p, table._parent)
            p2 = paragraph.insert_paragraph_before()
            p2.text = "отсутствует"
            table._element.getparent().remove(table._element)

            return

        first_row = table.rows[0]
        last_row = table.rows[-1]

        cells_eval = [i.text.strip() for i in last_row.cells]

        self.remove_row(table, first_row)
        self.remove_row(table, last_row)

        for row_index, item in enumerate(data):
            row = table.add_row()
            print(item)
            for cell_index, cell in enumerate(cells_eval):
                func = cells_eval[cell_index].replace('‘', "'").replace('’', "'")
                if func == '[counter]':
                    row.cells[cell_index].text = str(row_index + 1)
                elif func == '[item]':
                    row.cells[cell_index].text = str(item)
                elif func.startswith('[') and func.endswith(']'):
                    result = eval(func[1:-1])
                    if isinstance(result, bool):
                        if result:
                            row.cells[cell_index].text = '+'
                    elif result is not None:
                        row.cells[cell_index].text = str(result)
                else:
                    row.cells[cell_index].text = func
