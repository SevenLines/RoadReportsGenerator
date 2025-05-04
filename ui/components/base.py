

from api.contexts.state import StateContext


class BaseComponent:
    manager = None
    context_key:str

    def __init__(self):
        self.container = self.get_container()
        StateContext.subscribe(self.context_key,self.get_context_value())
        self.render()

    def get_context_value(self):
        value = StateContext.get_value(self.context_key)
        if value is None:
            return self.update
        else:
            return value

    def get_container(self):
        pass

    def render(self):
        pass

    def update(self,*_):
        self.container.clear()
        self.render.refresh()