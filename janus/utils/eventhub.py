import threading

class EventType:
    TOOLBAR_CHANGE_SELECTED = "toolbar_change_selected"
    ALIGN_BEAMOFFSET_TO_BEAMPROFILE = "align_beamoffset_to_beamprofile"

class Event:
    def __init__(self, type, data = None):
        self.type = type
        self.data = data
        self.sender_thread = threading.get_ident()

class EventHub:
    def __init__(self):
        self._callbacks = {}

    def register(self, type, callback):
        if not type in self._callbacks:
            self._callbacks[type] = []
        self._callbacks[type].append({"cb": callback, "tid": threading.get_ident()})

    def unregister(self, callback):
        for key in self._callbacks:
            cbs = self._callbacks[key]
            cbs[:] = [tup for tup in cbs if tup["cb"] != callback]

    def send(self, event):
        if event.type not in self._callbacks:
            return
        cbs = self._callbacks[event.type]
        if not isinstance(cbs, list):
            return
        for cb in cbs:
            if cb["tid"] != event.sender_thread:
                raise RuntimeError("listener was not registered from the same thread as the event sender. this could indicate an error, all events have to have handled in the main thread")
            cb["cb"](event)


hub = EventHub()
def global_event_hub():
    return hub