import sys
import random
import math
sys.path.append('generators')

from generators.auth import Auth

# Markov variables
X1 = 0
X2 = 0
X3 = 0
b = 0.5
c = (1/15) * 15
d = (1/3, 1/3, 1/3, 1/2)

# Configuration variables
CHOOSE_MUTATION = 0.5
PACKET_SELECTION_UNIFORM_DISTRIBUTION = 1
FUZZING_STATE_UNIFORM_DISTRIBUTION = 1

# Other parameters
FUZZING_INTENSITY = 0.1
CONSTRUCTION_INTENSITY = 3

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

# Calculate X3 from the fuzzing intensity fi and 
# construction intensity ci
def calculate_X3(fi = 0.1, ci = 3):
    global X3
    num = 1
    denom = 1 + RNG(RND(math.log(1 + ci * fi)))
    X3 = num / denom

# Parse the supplied config file
def parse_config_file(config):
    global CHOOSE_MUTATION
    global PACKET_SELECTION_UNIFORM_DISTRIBUTION
    global FUZZING_STATE_UNIFORM_DISTRIBUTION
    for line in config:
        # Only valid key-value pairs
        line = line.strip()
        line = line.replace(" ","")
        if len(line) == 0 or line[0] == '#':
            continue
    
        # Split into key-value pairs
        arg = line.split("=")
        if len(arg) != 2:
            continue

        if arg[0] == 'CHOOSE_MUTATION':
            CHOOSE_MUTATION = float(arg[1])

        if arg[0] == 'PACKET_SELECTION_UNIFORM_DISTRIBUTION':
            PACKET_SELECTION_UNIFORM_DISTRIBUTION = int(arg[1])

        if arg[0] == 'FUZZING_STATE_UNIFORM_DISTRIBUTION':
            FUZZING_STATE_UNIFORM_DISTRIBUTION = int(arg[1])
        

def main():
    # Get config file
    try:
        config_f = open(sys.argv[1], 'r')
        config = config_f.readlines()
        parse_config_file(config)
        config_f.close()
    except (FileNotFoundError, IndexError):
        print("Please provide a valid config file")
        exit(-1)

    print(PACKET_SELECTION_UNIFORM_DISTRIBUTION)

    # calculate_X1()
    # calculate_X2()
    # calculate_X3()    

if __name__ == "__main__":
    main()