import os
from api.contexts.state import StateContext
from api.managers.base import BaseManager
from docxtpl import DocxTemplate
import os
from sqlalchemy import insert, select
from models import Template, TemplateVariable,Connection
from api.db import SQLiteDB
from api.contexts.decorator import change_state
# class TemplateVariablesManager(BaseManager):
#     """
#     Менеджер Шаблонов
#     """
#     path = "stores/template_variables.json"
#     object_name = "templates"

#     def get_object(self, name:str):
#         form_var = {}
#         objects = self.get_objects()
#         template_vars = self.get_template_vars(name)
#         file_vars =  next((o["variables"] for o in objects if o.get("name") == name), {})
#         form_var = {var: file_vars.get(var) for var in template_vars}
#         return form_var
    




class TemplateVariablesManager:
    db = SQLiteDB()
    

    def get_object(self, template_name: str):
        """Получить все переменные шаблона с их значениями (если есть)"""

        if template_name is None:
            return None
        print(template_name)
        template_path = os.path.join('templates', template_name)

        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Шаблон {template_path} не найден.")

        doc = DocxTemplate(template_path)
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

        with self.db.session() as session:
            template = session.execute(
                select(Template).where(Template.name == template_name)
            ).scalar_one_or_none()

            if not template:
                return {var: None for var in undeclared_variables}

            variables_in_db = session.execute(
                select(TemplateVariable).where(TemplateVariable.template_id == template.id)
            ).scalars().all()

            db_variables_map = {v.name: v.value for v in variables_in_db}

            result = {var: db_variables_map.get(var, None) for var in undeclared_variables}

            return result

    def save_variables(self, template_name: str, variables: dict):
        """
        Сохраняет переданные переменные в базу.
        variables — это словарь {имя_переменной: значение}
        """
        with self.db.session() as session:
            # Ищем или создаем шаблон
            template = session.execute(
                select(Template).where(Template.name == template_name)
            ).scalar_one_or_none()

            if not template:
                template = Template(name=template_name)
                session.add(template)
                session.flush()  # Получаем template.id

            # Сначала получим все существующие переменные из базы
            existing_variables = session.execute(
                select(TemplateVariable).where(TemplateVariable.template_id == template.id)
            ).scalars().all()

            existing_variables_map = {v.name: v for v in existing_variables}

            for var_name, var_value in variables.items():
                if var_name in existing_variables_map:
                    # Обновляем значение
                    existing_variables_map[var_name].value = var_value
                else:
                    # Создаем новую запись
                    new_var = TemplateVariable(
                        template_id=template.id,
                        name=var_name,
                        value=var_value
                    )
                    session.add(new_var)

            session.commit()

class ConnectionManager:
    db = SQLiteDB()
    """
    Менеджер подключений к БД
    """
    def get_objects(self):
        with self.db.session() as session:
            results = session.execute(select(Connection)).scalars().all()
            return results

    @change_state("connection_history")
    def add_object(self,object:dict):
        with self.db.session() as session:
            session.execute(
                insert(Connection).values(**object)
            )
            session.commit()
            
    def get_object(self,id:int):
        with self.db.session() as session:
            return session.execute(
                select(Connection).where(
                    Connection.id == id
                )
            ).scalar_one_or_none()






class TemplateManager(BaseManager):
    path = "templates"

    def get_objects(self):
        templates = os.listdir(self.path)
        return templates
    
    def add_object(self, object):
        with open(f"{self.path}/{object.name}",'wb') as f:
            f.write(object.content.read())
        print(f"{self.path}.{object.name}")
            