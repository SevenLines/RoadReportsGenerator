import os
from api.contexts.state import StateContext
from api.managers.base import BaseManager
from docxtpl import DocxTemplate
import os
from sqlalchemy import insert, select
from models import Road, SavedFile, TemplateVariable,DBConnection
from api.db import RoadsDB, SQLiteDB


class TemplateVariablesManager(BaseManager):
    db = SQLiteDB
    model = TemplateVariable
    

    def get_queryset(self):
        return super().get_queryset().where(
            self.model.template_id == StateContext.get_value("current_template")
        )
                
    def get_objects(self):
        """Получить все переменные шаблона с их значениями (если есть)"""
        objs = super().get_objects()

        with self.db().session() as session:
            doc_path = session.execute(
                select(SavedFile.path)
                .where(
                    SavedFile.id==StateContext.get_value("current_template")
                    )
                ).scalar()
        doc = DocxTemplate(doc_path)
        undeclared_variables = doc.get_undeclared_template_variables()

        db_vars = {
            "road_title",
            "road_length",
            "covers",
            "signs",
            "light",
            "barriers",
            "tubes",
            "cross",
            "scheme",
        }

        undeclared_variables -= db_vars
        db_variables_dict = {v.name: v.value for v in objs}

        result = {}
        for var in undeclared_variables:
            try:
                val = int(db_variables_dict.get(var))
            except Exception:
                val = db_variables_dict.get(var)
            result[var] = val

        # result = {
        #     var: db_variables_dict.get(var) 
        #     for var in undeclared_variables
        # }
        print("res",result)
        return result

    def save_variables(self, template_name: str, variables: dict):
        """
        Сохраняет переданные переменные в базу.
        variables — это словарь {имя_переменной: значение}
        """
        with self.db().session() as session:
            # Ищем или создаем шаблон
            template = session.execute(
                select(SavedFile).where(
                    SavedFile.id == StateContext.get_value("current_template")
                    )
            ).scalar_one_or_none()

            # Сначала получим все существующие переменные из базы
            existing_variables = session.execute(
                select(TemplateVariable).where(
                    TemplateVariable.template_id == template.id
                    )
            ).scalars().all()

            existing_variables_map = {v.name: v for v in existing_variables}

            for var_name, var_value in variables.items():
                if var_name in existing_variables_map:
                    existing_variables_map[var_name].value = var_value
                else:
                    new_var = TemplateVariable(
                        template_id=template.id,
                        name=var_name,
                        value=var_value
                    )
                    session.add(new_var)

            session.commit()

class DBConnectionManager(BaseManager):
    """
    Менеджер подключений к БД
    """
    db = SQLiteDB
    model = DBConnection
    change_state_key = "connection_history"


class SavedFileTemplateManager(BaseManager):
    db = SQLiteDB
    model = SavedFile
    change_state_key = "template_list"

    def get_queryset(self):
        return super().get_queryset().where(self.model.is_connection == False)

class SavedFileConnectionManager(BaseManager):
    db = SQLiteDB
    model = SavedFile
    change_state_key = "access_connection_history"

    def get_queryset(self):
        return super().get_queryset().where(self.model.is_connection == True)



            