from api.managers.ms import RoadAccessManager, RoadDBManager
from api.contexts.state import StateContext



class RoadManagerFactory:

    def __new__(cls):
        current_connection = StateContext.get_value("current_connection")
        if not current_connection:
            return current_connection
        if current_connection.get("db"):
            return RoadDBManager()
        elif current_connection.get("access"):
            return RoadAccessManager()
        else:
            raise Exception("Неправильный конекст")
        