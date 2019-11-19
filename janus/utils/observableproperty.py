class ObservableProperty:
    def __init__(self, init):
        self._prop = init
        self._callbacks = []
        pass

    def register(self, callback):
        self._callbacks.append(callback)

    def unregister(self, callback):
        self._callbacks.remove(callback)

    def set(self, value):
        if self._prop is not None and type(self._prop) is not type(value):
            print("warning: overwriting ObservableProperty(prop: '{}', type: {}) with new value '{}' of type {}".format(self._prop, type(self._prop), value, type(value)))
        self._prop = value
        for cb in self._callbacks:
            cb(value)

    def get(self):
        return self._prop