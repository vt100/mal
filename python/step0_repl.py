def EVAL(x):
    return x

def READ(x):
    return x

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
        print i

rep()
