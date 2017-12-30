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
    elif isinstance(ast, MalVector):
        new_vector = MalVector()
        for i in ast.lst:
            new_vector.append(eval_ast(i, env))
        return new_vector
    elif isinstance(ast, MalList):
        #print "eval list"
        fst_ = ast[0]
        # print type(fst_)
        fst = fst_.name
        if fst == 'def!':
            v = eval_ast(ast[2], env)
            env.set(ast[1].name, v)
            return v
        elif fst == 'let*':
            new_env = Env(outer=env)
            bind_lst = ast[1]
            for i in range(bind_lst.length()/2):
                k = bind_lst[2*i]
                v = eval_ast(bind_lst[2*i+1], new_env)
                #print "setting %r=%r" % (k,v)
                new_env.set(k, v)
            return eval_ast(ast[2], new_env)
        else:
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

    return eval_ast(x, env)

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
