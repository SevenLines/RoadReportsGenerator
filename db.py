import configparser
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


class RoadsDB(object):
    db_driver = "mssql+pyodbc"

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.engine = create_engine(self.connection_string())

    def connection_string(self):
        c = self.config['connection']

        return f"{self.db_driver}://{c['user']}:{c['password']}@{c['host']}/{c['database']}?driver=SQL+Server"

    def session(self):
        return Session(self.engine)