import reader
from reader import read_form
from mal_types import *


repl_env = {'+': lambda a,b: a+b,
            '-': lambda a,b: a-b,
            '*': lambda a,b: a*b,
            '/': lambda a,b: int(a/b)}

def eval_ast(ast, env):
    if isinstance(ast, MalAtom):
        #print "env lookup:", ast.name
        return env[ast.name]
    elif isinstance(ast, MalList):
        print "eval list"

        # Evaluate form for function application
        new_list = MalList()
        for i in ast.lst:
            new_list.append(eval_ast(i, env))
        return APPLY(new_list)
    else:
        return ast

def APPLY(lst):
    #print "func apply", lst, type(lst.lst[0])
    return lst.first()(*lst.rest())

def EVAL(x, env):
    if isinstance(x, MalList):
        if x.length() == 0:
            return x
        else:
            return eval_ast(x, env)
    return x

def READ(x):
    r = reader.Reader(x)
    out = read_form(r)
    return out

def PRINT(x):
    print x

def rep():
    while True:
        try:
            i = raw_input("user> ")
        except EOFError:
            break
        if len(i) == 0:
            break
        PRINT(EVAL(READ(i), env=repl_env))

rep()
