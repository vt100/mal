from mal_types import *

class Env(object):
    def __init__(self, outer=None):
        self.outer = outer
        self.d = dict()

    def get(self, k):
        if k in self.d:
            return self.d[k]
        elif self.outer:
            # print "missed %r in %r" % (k, self.d)
            return self.outer.get(k)
        raise KeyError, (self.d, self.outer, k)

    def set(self, k, v):
        if isinstance(k, MalSymbol):
            k = k.name
        self.d[k] = v
