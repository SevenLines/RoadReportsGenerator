class StateContext:
    _state = {}
    _listeners = {}

    @classmethod
    def set_value(cls, key, value=None):
        cls._state[key] = value
        print(cls._listeners)
        if key in cls._listeners:
            print(key)
            for callback in cls._listeners[key]:
                callback(value)

    @classmethod
    def get_value(cls, key):
        return cls._state.get(key)

    @classmethod
    def subscribe(cls, key, callback):
        cls._listeners.setdefault(key, []).append(callback)

