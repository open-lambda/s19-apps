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

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def __binaryop__(a, b, func):
        a = array(a)
        b = array(b)
        obj = array(None, ch=[a.name, b.name], func=func)
        coordinator.calc_pie(obj)
        return obj

    def __add__(self, other):
        return Pie.__binaryop__(self, other, "add")

    def __radd__(self, other):
        return Pie.__binaryop__(other, self, "add")

    def __sub__(self, other):
        return Pie.__binaryop__(self, other, "sub")

    def __rsub__(self, other):
        return Pie.__binaryop__(other, self, "sub")

    def __mul__(self, other):
        return Pie.__binaryop__(self, other, "mul")

    def __rmul__(self, other):
        return Pie.__binaryop__(other, self, "mul")

    def __div__(self, other):
        return Pie.__binaryop__(self, other, "div")

    def __rdiv__(self, other):
        return Pie.__binaryop__(other, self, "div")


class Lampie:
    def __init__(self):
        self.var = {}  # name: str, Pie

    def set_pie(self, name, pie):
        self.var[name] = pie

    def get_pie(self, name):
        return self.var[name]

    def dumps(self):
        return dumps(self.var)

    def loads(self, obj):
        self.var = loads(obj)

    def __str__(self):
        return str(self.var)

    def __repr__(self):
        return self.__str__()


def calc_pie(cord, pie):
    if pie.type == "const":
        return
    if pie.type == "input":  # input the value from file
        value = cord.load_data()
        pie.value = value
        return
    # if pie.type == "output":
    if not cord.delay:
        pies = [cord.get_pie(i) for i in pie.children_name]
        for p in pies:
            cord.calc_pie(p)
        func = get_func(pie.func)
        value = func(*[p.value for p in pies])
        pie.value = value


def load_data(path):
    
    pass


class LampieClient:
    def __init__(self, lampie=None, delay=False):
        self.lampie = lampie or Lampie()
        self.delay = delay

    def dumps(self):
        obj = {"lampie": self.lampie.dumps()}
        return json_dumps(obj)

    def loads(self, obj):
        obj = jsonpickle.loads(obj)
        self.lampie.loads(obj['lampie'])

    def set_pie(self, name, pie):
        self.lampie.set_pie(name, pie)

    def get_pie(self, name):
        return self.lampie.get_pie(name)

    def calc_pie(self, pie):
        calc_pie(self, pie)

    def load_data(self):
        # Upload data
        pass


class LampieServer:
    def __init__(self, lampie=None, delay=False):
        self.lampie = lampie or Lampie()
        self.delay = delay

    def dumps(self):
        obj = {"lampie": self.lampie.dumps()}
        return json_dumps(obj)

    def loads(self, obj):
        obj = jsonpickle.loads(obj)
        self.lampie.loads(obj['lampie'])

    def set_pie(self, name, pie):
        self.lampie.set_pie(name, pie)

    def get_pie(self, name):
        return self.lampie.get_pie(name)

    def calc_pie(self, pie):
        calc_pie(self, pie)

    def load_data(self):
        # 1. Local Schema:
        # 2. HTTP Request: http(s):// ...
        # 3. Object Storage: psql:????
        pass


def Client(lampie=None):
    o = LampieClient(lampie)
    global coordinator
    coordinator = o
    return o


def Server(lampie=None):
    o = LampieServer(lampie)
    global coordinator
    coordinator = o
    return o


coordinator = Client()

counter = 0

dumps = cloudpickle.dumps
loads = cloudpickle.loads
json_dumps = jsonpickle.dumps
json_loads = jsonpickle.loads


def array(v, ch=None, func=None):
    if isinstance(v, Pie):
        return v

    def new_name():
        global counter
        counter += 1
        return str(counter)

    n = new_name()
    if isinstance(v, list):
        v = np.array(v)
    return Pie(n, v, ch, func)


func_dict = {
    "add": np.add,
    "sub": np.subtract,
    "mul": np.multiply,
    "div": np.divide
}


def get_func(foo):
    """foo: str or lambda"""
    if isinstance(foo, str) and foo in func_dict:
        return func_dict[foo]
    return foo
