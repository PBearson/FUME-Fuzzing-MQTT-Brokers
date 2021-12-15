import globals as g

def verbose_print(string):
    if g.VERBOSITY >= 2:
        print(string)

def normal_print(string):
    if g.VERBOSITY >= 1:
        print(string)

def debug_print(string):
    if g.VERBOSITY >= 3:
        print(string)