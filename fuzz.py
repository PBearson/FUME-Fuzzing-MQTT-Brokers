import sys
import random
import math
sys.path.append('generators')

from generators.auth import Auth

# Our Markov variables
X1 = 0
X2 = 0
X3 = 0

def RND(x):
    return round(x)

def RNG(x):
    return random.randint(0, x)

# Calculate X1 from the construction intensity ci
def calculate_X1(ci = 3):
    global X1
    num = 1
    denom = 1 + RNG(RND(ci))
    X1 = num / denom

# Calculate X2 from the fuzzing intensity fi
def calculate_X2(fi = 0.1):
    global X2
    num = 1
    denom = 1 + RNG(RND(100 * fi))
    X2 = num / denom

def calculate_X3(fi = 0.1, ci = 3):
    global X3
    num = 1
    denom = 1 + RNG(RND(math.log(1 + ci * fi)))
    X3 = num / denom

def main():
    # Get config file
    try:
        config = open(sys.argv[1], 'r')
        config.close()
    except FileNotFoundError:
        print("Please provide a valid config file")
        exit(-1)

    calculate_X1()
    calculate_X2()
    calculate_X3()
    print(X1, X2, X3)
    

if __name__ == "__main__":
    main()