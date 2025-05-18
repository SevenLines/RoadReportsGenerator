import configparser
from api.contexts.state import StateContext
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from nicegui import ui
class BaseDB:

    db_driver: str

    def __init__(self):
        self.connection = StateContext.get_value("current_connection")
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
        self.engine = create_engine(self.connection_string())
        print("engine_created")


    def session(self):
        return Session(self.engine)
    
    def connection_string(self):
        raise NotImplementedError


class RoadsDB(BaseDB):
    db_driver = "mssql+pyodbc"

    def connection_string(self):
        conf_conn = self.config["connection"]
        c = self.connection.get("db")
        # print(f"{self.db_driver}://{c.user}:{c.password}@{c.host}/{c.db_name}?driver={conf_conn['driver']}")
        return f"{self.db_driver}://{c.user}:{c.password}@{c.host}/{c.db_name}?driver={conf_conn['driver']}"


class RoadsDBAccess(BaseDB):
    db_driver = "access+pyodbc"

    def connection_string(self):
        path = self.connection.get("access").path.replace("/","\\")
        return f"{self.db_driver}:///?odbc_connect=DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={path}"


class SQLiteDB(BaseDB):
    db_driver = "sqlite"

    def connection_string(self) -> str:
        db_path ="database.db"  # Путь к файлу базы
        return f"{self.db_driver}:///{db_path}"
    