import numpy as np
from enum import Enum
import logging
from numpy import ndarray


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