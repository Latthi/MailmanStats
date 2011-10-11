class T:
    def __init__(self, *objs):
        self.objs = []
        for obj in objs:
            self.add(obj)
    def add(self, *objs):
        for obj in objs:
            self.objs.append(obj)
    def add_objects(self, list):
        for obj in list:
            self.add(obj)
    def iterate(self):
        return Iterator(self)
    def list(self):
        return self.objs
    def __getitem__(self, idx):
        return self.objs[idx]
    def nth(self, idx):
        return self.objs[idx]
class Iterator:
    def __init__(self, set_):
        self.set = set_
        self.idx = 0
    def reset(self):
        self.idx = 0
    def next(self):
        val = self.set.objs[self.idx]
        self.idx = self.idx + 1
        if self.idx >= len(self.set.objs):
            self.idx = 0
        return val

    
