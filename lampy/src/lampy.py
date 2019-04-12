import numpy as np
from enum import Enum
import logging
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
OUTPUT_NODE = [LampyStatus.Output_Undefined,LampyStatus.Output_Empty,LampyStatus.Output_Loading,
               LampyStatus.Output_Running,LampyStatus.Output_Done]
DONE_NODE = [LampyStatus.Output_Done, LampyStatus.Input_Done, LampyStatus.Const]

def _array(val=None, children=None, op=None):
    """Internal method to create a new array.
    Return val: a triple : (val, data_src, status)
    """
    if children is not None:
        return (None, None, LampyStatus.Output_Empty)
    # Empty Node
    if val is None:
        return (np.array([]), None, LampyStatus.Empty)
    # Const Node
    if isinstance(val, (list, np.ndarray)):
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
        return x == (1, )

    @staticmethod
    def _is_vector(x: tuple):
        return len(x) == 1

    @staticmethod
    def _fix_shape(x: tuple, y: tuple):
        maxlen = max(len(x), len(y))
        if maxlen == 0:
            return ((0,), (0,)) # Invalid return
        generator = lambda x, len_x: tuple([x[i] if i < len_x else 1 for i in range(len_x)])
        m = generator(x, len(x))
        n = generator(y, len(y))
        return m, n


    @staticmethod
    def _shape_op(x: tuple, y: tuple):
        # TODO: This is absolutely not a good idea, but let's jut keep it that way -- otherwise goto C level and see
        #  the broadcast machenism.
        if x == (0,) or y == (0,):
            return (0, )
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


class LampyOperator(Enum):
    add_operator = _LampyAddOperator()
    mul_operator = _LampyMulOperator()


class LampyObject:
    def __init__(self, val=None, children=None, op=None):
        self._chs = children if children is not None else []
        self._op: _LampyOperator = op
        self._val, self._data_src, self._status = _array(val, children)

        # Cache value -- could be dirty
        self._shape = None
        # self._meta = None

    @property
    def status(self) -> LampyStatus:
        return self._status

    @property
    def children(self):
        return self._chs

    def is_type(self, *args):
        for nodeset in args:
            if not isinstance(nodeset, list):
                nodeset = [nodeset]
            if self.status in nodeset:
                return True
        return False

    def operate(self, *args):
        try:
            result = self._op(*args)
            self._val = result
            return result
        except:
            assert( False, "Operation failed")

    @property
    def shape(self):
        if self.is_done():
            return self._val.shape
        if self._shape:
            return self._shape
        # Children Shape retrieve
        shapes = [ ch.shape for ch in self.children ]
        self._shape = self._op.shape(*shapes)
        return self._shape

    # Retrieve the full data
    @property
    def value(self):
        if not self.is_done():
            if self.is_type(INPUT_NODE):
                # TODO: Input all things from data_src
                pass
            elif self.is_type(OUTPUT_NODE):
                # Recursively calculate children's value
                ch_vals = [ch.value for ch in self.children]
                self.operate(*ch_vals)
            self._mark_done()
        return self._val

    # See _val in any case
    def async_value(self):
        return self._val

    # Return current outcome
    def is_done(self):
        return self.is_type(DONE_NODE)

    def _mark_done(self):
        if self.is_type(INPUT_NODE):
            self._status = LampyStatus.Input_Done
            return
        if self.is_type(OUTPUT_NODE):
            self._status = LampyStatus.Output_Done
            return


    def __add__(self, other):
        op = LampyOperator.add_operator.value
        return LampyObject(children=[self, other], op=op)

    def __mul__(self, other):
        op = LampyOperator.mul_operator.value
        return LampyObject(children=[self, other], op=op)

    def __str__(self):
        return f"LampyObject({self.value}, status={self.status.name})"

        return self.val

    def __add__(self, obj):
        return LamObject(val=None, children=[self, obj])

    def __str__(self):
        return self.val.__str__()