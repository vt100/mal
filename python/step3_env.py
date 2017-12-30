import traceback
import reader
from reader import read_form
from mal_types import *
from env import Env

repl_env = Env()

for (k,v) in {'+': lambda a,b: a+b,
              '-': lambda a,b: a-b,
              '*': lambda a,b: a*b,
              '/': lambda a,b: int(a/b)}.items():
    repl_env.set(k,v)

def eval_ast(ast, env):
    if isinstance(ast, MalAtom):
        #print "env lookup:", ast.name
        return env.get(ast.name)
    elif isinstance(ast, MalList):
        new_obj = type(ast)()
        for i in ast.lst:
            new_obj.append(eval_ast(i, env))
        return new_obj
    else:
        return ast

def APPLY(lst):
    #print "func apply", lst, type(lst.lst[0])
    return lst.first()(*lst.rest())

def EVAL(x, env):
    if type(x) != MalList: # not isinstance(x, MalList):
        return eval_ast(x, env)

    if x.length() == 0:
        return x

    fst_ = x[0]
    fst = fst_.name

    if fst == 'def!':
        v = EVAL(x[2], env)
        env.set(x[1].name, v)
        return v
    elif fst == 'let*':
        new_env = Env(outer=env)
        bind_lst = x[1]
        for i in range(bind_lst.length()/2):
            k = bind_lst[2*i]
            v = EVAL(bind_lst[2*i+1], new_env)
            #print "setting %r=%r" % (k,v)
            new_env.set(k, v)
        return EVAL(x[2], new_env)
    else:
        # Evaluate form for function application
        new_list = MalList()
        for i in x.lst:
            new_list.append(EVAL(i, env))
        return APPLY(new_list)


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
        try:
            PRINT(EVAL(READ(i), env=repl_env))
        except:
            traceback.print_exc()

rep()
