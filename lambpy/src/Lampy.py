from enum import Enum
from functools import reduce

import numpy as np


class LamStatus(Enum):
    CONST = 0  # A Defined Constant
    DATA_SRC = 1  # A defined data source node
    DATA_DES = 2  # A to-be-calculated node
    DATA_SRC_FETCHED = 3  # A data source node who fetched the matrix and loaded the data
    DATA_DES_COMPUTED = 4  # A data dest node who computed the result


class LamObject():

    def __init__(self, val=None, children=None):

        self.children = children or []
        self.data_src = None
        self.status = None
        self.val = None  # Declaration here

        self.init_val(val)

    def init_val(self, val):
        """Determine what is the status of the node"""
        if isinstance(val, np.ndarray):
            # The node is a constant node
            self.status = LamStatus.CONST
            self.val = val

        elif isinstance(val, (list,)):
            # The node is a constant node
            self.status = LamStatus.CONST
            self.val = np.array(val)
        
    def run(self):
        if not len(self.children):
            return self.val
        for i in self.children:
            i.run()
        sum = self.children[0].val
        for i in self.children[1:]:
            sum += i.val
        self.val = sum
        return sum
        
        
    def __add__(self, obj):
        return LamObject(val=None, children=[self, obj])
    
    def __str__(self):
        return self.val.__str__()

#     def __repr__(self):
#         return self.val.__str__()

a = LamObject([1,2,3])
b = LamObject([1,2,3])
d = LamObject([4])

c = a + b + d