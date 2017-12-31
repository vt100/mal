from mal_types import *
import re
tre = re.compile(r"""[\s,]*(~@|[\[\]{}()'`~^@]|"(?:[\\].|[^\\"])*"?|;.*|[^\s\[\]{}()'"`@,;]+)""")

def tokenize(s):
    return [t for t in re.findall(tre, s) if t[0] != ';']

class Reader(object):
    def __init__(self, txt):
#        self.pattern = r'[\s,]*(~@|[\[\]{}()'`~^@]|"(?:\\.|[^\\"])*"|;.*|[^\s\[\]{}('"`,;)]*)'
        self.txt = txt
        self.tokens = tokenize(txt)
        self.idx = 0

    def peek(self):
        if self.idx >= len(self.tokens):
            return None
        return self.tokens[self.idx]

    def next(self):
        if self.idx >= len(self.tokens):
            return None
        res = self.tokens[self.idx]
        self.idx += 1
        return res


def read_str(s):
    r = Reader(s)
    read_form(r)

def read_form(reader):
    fst = reader.peek()

    parsers = {'(': read_list,
               '[': read_vector}

    func = parsers.get(fst, read_atom)
    return func(reader)

def read_list(reader):
    assert reader.next() == "("
    res = MalList()
    while reader.peek() and reader.peek()[0] != ")":
        item = read_form(reader)
        res.append(item)
    close_bracket = reader.next()
    if close_bracket is None:
        return "EOF"
    assert close_bracket == ")", reader.tokens
    return res

def read_vector(reader):
    assert reader.next() == "["
    res = MalVector()
    while reader.peek() and reader.peek()[0] != "]":
        item = read_form(reader)
        res.append(item)
    close_bracket = reader.next()
    if close_bracket is None:
        return "EOF"
    assert close_bracket == "]", reader.tokens
    return res

def read_atom(reader):
    token = reader.next()
    if token is None:
        return MalNone

    if token[0] in "-0123456789":
        return int(token)

    if token == "true":
        return MalBool(True)

    if token == "false":
        return MalBool(False)

    if token == "nil":
        return MalNil()

    return MalSymbol(token)
