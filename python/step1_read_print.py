import reader
from reader import read_form

def EVAL(x):
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
        PRINT(EVAL(READ(i)))

rep()
