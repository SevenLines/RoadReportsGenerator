from db import RoadsDB
from models import Road


class RoadRetreiver:

    def __init__(self):
        self.roads = []
        self.chosen_id = []
    
    def roads_to_dict(self):
        self.roads = [
            {
                'id':r.id,
                'name':r.Name,
            } 
        for r in self.roads
        ]

    def get_roads(self):
        with RoadsDB().session() as session:
            self.roads = session.query(Road).all()
            self.roads_to_dict()
        
    def get_roads_by_name(self, name):
        with RoadsDB().session() as session:
            self.roads = session.query(Road).filter(Road.Name.like(name+'%')).all()
            self.roads_to_dict()
        



