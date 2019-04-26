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


