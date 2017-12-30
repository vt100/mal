from mal_types import *

class Env(object):
    def __init__(self, outer=None):
        self.outer = outer
        self.d = dict()

    def get(self, k):
        if k in self.d:
            return self.d[k]
        elif self.outer:
            #print self.d
            return self.outer.get(k)
        raise KeyError, self.d

    def set(self, k, v):
        if isinstance(k, MalAtom):
            k = k.name
        self.d[k] = v
