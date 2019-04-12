import json
from enum import Enum

import numpy as np
import requests
from numpy import ndarray


class LampyStatus(Enum):
    # Empty Node
    Empty = 0

    # Const node
    Const = 1

    # Output nodes
    Output_Undefined = 10
    Output_Empty = 11
    Output_Running = 12
    Output_Loading = 13
    Output_Done = 14

    # Input nodes
    Input_Empty = 21
    Input_Loading = 22
    Input_Done = 23


CONST_NODE = [LampyStatus.Const]
INPUT_NODE = [LampyStatus.Input_Empty, LampyStatus.Input_Loading, LampyStatus.Input_Done]
OUTPUT_NODE = [LampyStatus.Output_Undefined, LampyStatus.Output_Empty, LampyStatus.Output_Loading,
               LampyStatus.Output_Running, LampyStatus.Output_Done]
DONE_NODE = [LampyStatus.Output_Done, LampyStatus.Input_Done, LampyStatus.Const]


def array(val):
    # If val is a LampyObject, we return the object -- not renew it -- observe the numpy practice.
    if isinstance(val, LampyObject):
        return val
    return LampyObject(val)


def _array(val=None, children=None, op=None):
    """Internal method to create a new array.
    Return val: a triple : (val, data_src, status)
    """
    if children is not None:
        return (None, None, LampyStatus.Output_Empty)
        # return (None, None, LampyStatus.Output_Empty)
    # Empty Node
    if val is None:
        return (np.array([]), None, LampyStatus.Empty)
    # Const Node
    if isinstance(val, (list, np.ndarray, int, bool, complex, float)):
        return (np.array(val), None, LampyStatus.Const)
    # Data input node
    if isinstance(val, (str)):
        return (None, val, LampyStatus.Input_Empty)


class _LampyOperator:
    def __init__(self, op, shape_op):
        self._op = op
        self._shape_op = shape_op

    def __call__(self, *args):
        return self._op(*args)

    def shape(self, *args):
        return self._shape_op(*args)


class _LampyAddOperator(_LampyOperator):
    @staticmethod
    def _shape_op(x: tuple, y: tuple):
        return max(x, y)

    @staticmethod
    def _op(x: ndarray, y: ndarray):
        return x + y

    def __init__(self):
        super(_LampyAddOperator, self).__init__(
            op=self._op, shape_op=self._shape_op,
        )

    def __call__(self, *args):
        return self._op(*args)


class _LampyMulOperator(_LampyOperator):
    @staticmethod
    def _is_scalar(x: tuple):
        return x == (1,)

    @staticmethod
    def _is_vector(x: tuple):
        return len(x) == 1

    @staticmethod
    def _fix_shape(x: tuple, y: tuple):
        maxlen = max(len(x), len(y))
        if maxlen == 0:
            return ((0,), (0,))  # Invalid return
        generator = lambda x, len_x: tuple([x[i] if i < len_x else 1 for i in range(maxlen)])
        m = generator(x, len(x))
        n = generator(y, len(y))
        return m, n

    @staticmethod
    def _shape_op(x: tuple, y: tuple):
        # TODO: This is absolutely not a good idea, but let's jut keep it that way -- otherwise goto C level and see
        #  the broadcast machenism.
        if x == (0,) or y == (0,):
            return (0,)
        # Has scalar
        if _LampyMulOperator._is_scalar(x):
            return y
        if _LampyMulOperator._is_scalar(y):
            return x

        # Both are vector
        if _LampyMulOperator._is_vector(x) and _LampyMulOperator._is_vector(y):
            if x == y:
                return x
            raise Exception("Shape not match")

        # Matrix Multiplication
        m, n = _LampyMulOperator._fix_shape(x, y)
        if m[1] == n[0]:
            return (m[0], n[1])
        raise Exception("Shape not match")

    @staticmethod
    def _op(x: ndarray, y: ndarray):
        return x * y

    def __init__(self):
        super(_LampyMulOperator, self).__init__(
            op=self._op, shape_op=self._shape_op,
        )

    def __call__(self, *args):
        return self._op(*args)


class _LampyDotOperator(_LampyOperator):
    @staticmethod
    def _shape_op(x: tuple, y: tuple):
        return tuple([1]) # Guarantee a tuple return

    @staticmethod
    def _op(x: ndarray, y: ndarray):
        return x.dot(y)

    def __init__(self):
        super(_LampyDotOperator, self).__init__(
            op=self._op, shape_op=self._shape_op,
        )

    def __call__(self, *args):
        return self._op(*args)


class _LampyConvOperator(_LampyOperator):
    @staticmethod
    def _shape_op(x: tuple, y: tuple):
        # TODO: This is wrong. Implement this.
        return max(x, y)

    @staticmethod
    def _op(x: ndarray, y: ndarray, mode='same'):
        return np.convolve(x, y, mode=mode)

    def __init__(self):
        super(_LampyConvOperator, self).__init__(
            op=self._op, shape_op=self._shape_op,
        )

    def __call__(self, *args, **kwargs):
        return self._op(*args, **kwargs)


class LampyOperator(Enum):
    add_operator = _LampyAddOperator()
    mul_operator = _LampyMulOperator()
    dot_operator = _LampyDotOperator()
    conv_operator = _LampyConvOperator()


def convolve(x: 'LampyObject', y: 'LampyObject', mode='same'):
    # TODO: mode='full' is the default.
    return LampyObject(None, [x, y], op=LampyOperator.conv_operator)



class LampyObject:
    def __init__(self, val=None, children=None, op=None):
        self._chs = children if children is not None else []
        self._op: _LampyOperator = op
        self._val, self._data_src, self._status = _array(val, children)

        # Cache value -- could be dirty
        self._shape = None
        # self._meta = None

    # Object Property
    @property
    def status(self) -> LampyStatus:
        return self._status

    @property
    def children(self):
        return self._chs

    def _is_type(self, *args):
        for nodeset in args:
            if not isinstance(nodeset, list):
                nodeset = [nodeset]
            if self.status in nodeset:
                return True
        return False

    # Schedule-able Task Handler
    def _operate(self, *args):
        try:
            result = self._op(*args)
            self._val = result
            return result
        except:
            assert (False, "Operation failed")

    def _get_url_data_content(self, url):
        pass

    def _resolve_content_from_data_src(self, data):
        val = None

        # TODO: Make the numpy load function here - to decode the string instead of loading a file.
        # try:
        #     val = np.load(data)
        #     return val
        # except:
        #     print(f"[Debug] Not numpy file.")

        try:
            val = np.array(json.loads(data))
            return val
        except:
            print(f"[Debug] Not json file.")

        raise Exception("Not parseable data")

    def _read_data_src(self):
        if not self._is_type([LampyStatus.Input_Empty]):
            return
        # self._status = LampyStatus.Input_Loading
        # TODO: Support both local and remote access
        req = requests.get(self._data_src)
        data = self._resolve_content_from_data_src(req.content)
        self._val = data
        # self._status = LampyStatus.Input_Done

    @property
    def shape(self):
        """Resolve shape of the object"""
        if self.is_done():
            return self._val.shape
        # if self._shape:
        #     return self._shape
        # Children Shape retrieve
        shapes = [ch.shape for ch in self.children]
        self._shape = self._op.shape(*shapes)
        return self._shape

    @property
    def value(self):
        """Resolve value of the object"""
        if not self.is_done():
            if self._is_type(INPUT_NODE):
                # TODO: Dispatch remote task for computation
                # TODO: Input all things from data_src
                self._read_data_src()
            elif self._is_type(OUTPUT_NODE):
                # Recursively calculate children's value
                ch_vals = [ch.value for ch in self.children]
                # TODO: Dispatch this job to the scheduler
                self._operate(*ch_vals)
                # TODO: Block and wait for the job
            self._mark_done()
        return self._val

    @property
    def async_value(self):
        return self._val

    # Automaton status methods
    def is_done(self):
        return self._is_type(DONE_NODE)

    def _mark_done(self):
        if self._is_type(INPUT_NODE):
            self._status = LampyStatus.Input_Done
            return
        if self._is_type(OUTPUT_NODE):
            self._status = LampyStatus.Output_Done
            return

    def __radd__(self, other):
        return self.__add__(other)

    # Python Native Operator Capture Function
    def __add__(self, other):
        if not isinstance(other, LampyObject):
            other = array(other)
        op = LampyOperator.add_operator.value
        return LampyObject(children=[self, other], op=op)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __mul__(self, other):
        if not isinstance(other, LampyObject):
            other = array(other)
        op = LampyOperator.mul_operator.value
        return LampyObject(children=[self, other], op=op)

    def dot(self, other):
        if not isinstance(other, LampyObject):
            other = array(other)
        op = LampyOperator.dot_operator.value
        return LampyObject(children=[self, other], op=op)

    def conv(self, other, mode='same'):
        if not isinstance(other, LampyObject):
            other = array(other)
        op = LampyOperator.conv_operator.value
        # TODO: op = _LampyConvOperator(mode=mode) # Customize Operator
        return LampyObject(children=[self, other], op=op)


    # Representation
    def __str__(self):
        # TODO: Refer to arrayprint to see how to pretty-print LampyObject
        value = repr(self.value)
        status = self.status.name
        return f"LampyObject(status={status}, value={value})"
