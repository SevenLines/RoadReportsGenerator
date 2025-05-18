
from sqlalchemy import insert, select
from api.contexts.state import StateContext
from api.db import SQLiteDB


class BaseManager:
    db = SQLiteDB
    change_state_key:str
    model = None # Модель


    def get_queryset(self):
        return select(self.model)

    def get_objects(self):
        with self.db().session() as s:
            return s.execute(self.get_queryset()).scalars().all()
        
    def add_object(self,object:dict[str,any]):
        with self.db().session() as s:
            s.execute(
                insert(self.model).values(**object)
            )
            s.commit()
        StateContext.set_value(self.change_state_key)

    def get_object(self,id:int):
        with self.db().session() as s:
            return s.execute(
                self.get_queryset()
                .where(self.model.id == id)
            ).scalar_one_or_none()