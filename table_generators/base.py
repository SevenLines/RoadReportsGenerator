from sqlalchemy import text, bindparam

from models import Attribute

POSITION_LEFT = -1
POSITION_RIGHT = 1
POSITION_BOTH = 0


class TableGeneratorBase(object):
    condition = ""
    title = ""

    def __init__(self, high_id, db):
        self.db = db
        self.high_id = high_id

    def prepare_data(self):
        with self.db.session() as s:
            items = list(s.execute(text(f"""
            EXEC ExelReport {self.high_id}, 1, {self.condition}, 0.000000, 615.000000, 1
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

                item_data = {
                    "id": item.ID_Attribute,
                    "name": item._asdict()['Название атрибута'],
                    "type": item.ID_Type_Attr,
                    "begin": item.Начало,
                    "end": item.Конец,
                    "position": position,
                    "format": item.ID_Format,
                    "params": {}
                }
                params = s.execute(text(f"""
                SELECT Params.ID_Param, Types_Description.Param_Name, Params.ValueParam, Params.Suffix FROM Params INNER JOIN Types_Description ON Params.ID_Param = Types_Description.ID_Param WHERE (Params.ID_Attribute = {item.ID_Attribute})  and Params.ID_RegDate=dbo.GetIndexDate(1,Params.ID_Param,Params.ID_Attribute) order by Params.ID_Param
                """))
                for p in params:
                    item_data['params'][p.Param_Name] = p.ValueParam

                result.append(item_data)
        return result
