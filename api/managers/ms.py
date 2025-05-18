


from api.db import RoadsDB, RoadsDBAccess
from api.managers.base import BaseManager
from models import Road




class RoadManager(BaseManager):
    model = Road
    change_state_key = "roads"

    def get_roads_by_name(self, name):
        with self.db.session() as session:
           return session.execute(
            self.get_queryset()
            .where(Road.Name.like(name + "%"))
        ).scalars().all()



class RoadDBManager(RoadManager):
    db = RoadsDB

class RoadAccessManager(RoadManager):
    db = RoadsDBAccess