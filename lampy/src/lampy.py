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
        try:
            self.val = np.array(json.loads(data))
            return
        except:
            print(f"[Debug] {url} not json object file either.")
        raise Exception(f'Data source not availble: {self.data_src}')

    def run_base(self):
        if self.status == LamStatus.DATA_DES:
            return
        if not len(self.children):
            if self.status == LamStatus.DATA_SRC:
                self.fetch()  # Fetch data here!
            return

    def run(self):
        # Leaf Node:
        #  1. Const Node:
        #  2. Data source node:
        self.run_base()
        if self.status is not LamStatus.DATA_DES:
            return

        # Internal Nodes: should all be DATA_DES
        for i in self.children:
            i.run()

        # Actual addition
        self.val = reduce(lambda x, y: x.val + y.val, self.children)

        return self.val

    def __add__(self, obj):
        return LamObject(val=None, children=[self, obj])

    def __str__(self):
        return self.val.__str__()