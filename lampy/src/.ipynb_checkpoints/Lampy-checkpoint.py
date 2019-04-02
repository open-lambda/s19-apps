class LamObject():
    def __init__(self, val=None, children=[]):
        self.children = children   # [LamObject]
        if isinstance(val, numpy.ndarray):
            self.val = val
        else:
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