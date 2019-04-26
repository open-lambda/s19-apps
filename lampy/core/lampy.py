from contextlib import contextmanager

import cloudpickle
import jsonpickle
import numpy as np


@contextmanager
def delay():
    global coordinator
    old = coordinator.delay
    try:
        coordinator.delay = True
        yield
    finally:
        coordinator.delay = old


# Global Variable -- should not be access by user eventually

class Pie:
    def __init__(self, name, value, children_name, func):
        self.name = name
        self.value = value
        self.children_name = children_name or []
        self.func = func or "add"
        coordinator.set_pie(name, self)

    @property
    def type(self):
        if isinstance(self.value, str):
            return "input"
        if self.value is not None:
            return "const"
        if isinstance(self.children_name, list) and len(self.children_name) > 0 and self.func:
            return "output"
        return "unknown"

    def get_value(self):
        if self.type != "const":
            global coordinator
            coordinator.calc_pie(self)
            pass
        pass

    def __str__(self):
        self.get_value()
        return "<%s [type=%s, name=%s] (%s)>" % (str(self.__class__), self.type, self.name, self.value)