import json


class BaseManager:
    path: str
    object_name: str
    objects = {}


    def get_objects(self):
        """
        Получаем обьекты
        """
        with open(self.path,'r') as f:
            data = json.loads(f.read())
        
        objects = data.get(self.object_name)

        return objects or []
    

    def add_object(self, object):
        """
        Добавляем обьект
        """
        data = self.get_objects()
        data[self.object_name].append(object)

        with open(self.path,'w') as f:
            f.write(json.dumps(data))