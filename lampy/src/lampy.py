import json
import shutil
from enum import Enum
from functools import reduce

import numpy as np
import requests


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

        elif isinstance(val, (str,)):
            # The node is a Data source node.
            # The data will have to be fetched later.
            self.status = LamStatus.DATA_SRC
            self.val = None
            self.data_src = val

        else:
            # The node is a Data destination node
            # The data will depend on other data_src / const nodes
            self.status = LamStatus.DATA_DES
            self.val = None
            self.data_src = None

    def fetch(self):
        # Dev Phase:
        #  3. Fetch only a portion of the file -> a meta node tell the server to pre-process the data and pre-fetch
        url = self.data_src
        # TODO: Issue a lambda call to get the data ready
        req = requests.get(url) # Blocking call for a resource
        data = req.content
        try:
            self.val = np.load(data)
            return
        except:
            print(f"[Debug] {url} not numpy object file. Try json parsing")

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