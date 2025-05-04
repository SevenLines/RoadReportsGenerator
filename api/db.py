import configparser
from api.contexts.state import StateContext
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from nicegui import ui
class BaseDB:

    db_driver: str

    def __init__(self):
        self.connection = StateContext.get_value("current_connection")
        print(self.connection)
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
        self.engine = create_engine(self.connection_string())


    def session(self):
        return Session(self.engine)
    
    def connection_string(self):
        raise NotImplementedError

class RoadsDB(BaseDB):
    db_driver = "mssql+pyodbc"

    def connection_string(self):
        conf_conn = self.config["connection"]
        c = self.connection

        return f"{self.db_driver}://{c.user}:{c.password}@{c.host}/{c.db_name}?driver={conf_conn['driver']}"


class RoadsDBAccess(BaseDB):
    db_driver = "access+pyodbc"


    def connection_string(self):
        c = self.config["connection"]

        return f"{self.db_driver}://e:\\Roads\\2024\\_\\1\\Хомутово - Братская.svpd"



class SQLiteDB(BaseDB):
    db_driver = "sqlite"

    def connection_string(self) -> str:
        c = self.config["connection"]
        db_path = c.get("db_path", "database.db")  # Путь к файлу базы
        return f"{self.db_driver}:///{db_path}"
    