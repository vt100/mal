class MalType(object):
    pass

class MalNone(MalType):
    def __str__(self):
        return ""

class MalList(MalType):
    def __init__(self):
        self.lst = list()
    def append(self, item):
        self.lst.append(item)
    def __str__(self):
        return "(%s)" %  " ".join([str(i) for i in self.lst])
    def length(self):
        return len(self.lst)
    def first(self):
        return self.lst[0]
    def rest(self):
        return self.lst[1:]
    def __getitem__(self, idx):
        return self.lst[idx]

class MalVector(MalList):
    def __str__(self):
        return "[%s]" %  " ".join([str(i) for i in self.lst])

class MalAtom(MalType):
    pass

class MalLambda(MalType):
    def __init__(self, body, bind_list, env, fn):
        self.body = body
        self.bind_list = bind_list
        self.env = env
        def func(*args):
            new_env = Env(outer=env)
            for (k,v) in zip(bind_list, args):
                new_env.set(k, v)
                return EVAL(body, new_env)
        self.fn = func


class MalNil(MalType):
    def __repr__(self):
        return "nil"

class MalBool(MalType):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return str(self.value).lower()

class MalSymbol(MalType):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        #return "atom(%s)" % self.name
        return self.name or ""
