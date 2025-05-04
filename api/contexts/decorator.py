
from api.contexts.state import StateContext


def change_state(state_key:str):
    def inner_decorator(func):
        def wrapper(*args,**kwargs):
            result = func(*args,**kwargs)
            StateContext.set_value(state_key)
            return result
        return wrapper
    return inner_decorator
