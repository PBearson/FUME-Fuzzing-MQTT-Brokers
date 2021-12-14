import sys
import random
import math
sys.path.append('generators')

from generators.auth import Auth

# Markov variables
X1 = 0.5
X2 = 0.5
X3 = 1
b = 0.5
c = [1/15] * 15
d = [1/3, 1/3, 1/3, 1/2]

# Configuration variables
CHOOSE_MUTATION = 0.5
PACKET_SELECTION_UNIFORM_DISTRIBUTION = 1
FUZZING_STATE_UNIFORM_DISTRIBUTION = 1

# Other parameters
FUZZING_INTENSITY = 0.1
CONSTRUCTION_INTENSITY = 3

# If 1, then the user supplied X1, X2, or X3 in the config file
user_supplied_X = [0, 0, 0]

# CONSTRUCTION_INTENSITY must be a non-negative integer
def validate_construction_intensity():
    global CONSTRUCTION_INTENSITY
    assert int(CONSTRUCTION_INTENSITY) == CONSTRUCTION_INTENSITY
    assert CONSTRUCTION_INTENSITY >= 0

# FUZZING_INTENSITY must be in the range [0...1]
def validate_fuzzing_intensity():
    global FUZZING_INTENSITY
    assert FUZZING_INTENSITY >= 0 and FUZZING_INTENSITY <= 1

# FUZZING_STATE_UNIFORM_DISTRIBUTION must be binary
def validate_fuzzing_state_uniform_distribution():
    global FUZZING_STATE_UNIFORM_DISTRIBUTION
    assert FUZZING_STATE_UNIFORM_DISTRIBUTION in [0, 1]

# PACKET_SELECTION_UNFIROM_DISTRIBUTION must be binary
def validate_packet_selection_uniform_distribution():
    global PACKET_SELECTION_UNIFORM_DISTRIBUTION
    assert PACKET_SELECTION_UNIFORM_DISTRIBUTION in [0, 1]

# CHOOSE_MUTATION must be in the range [0...1]
def validate_choose_mutation():
    global CHOOSE_MUTATION
    assert CHOOSE_MUTATION <= 1 and CHOOSE_MUTATION >= 0

# X1, X2, and X3 must be in the range [0...1]
def validate_X():
    global X1, X2, X3
    assert X1 <= 1 and X1 >= 0
    assert X2 <= 1 and X2 >= 0
    assert X3 <= 1 and X3 >= 0

# b must be in the range [0...1]
def validate_b():
    global b
    assert b <= 1 and b >= 0

# The values in c must sum to 1
def validate_c():
    global c
    sum = 0
    for ci in c:
        sum += ci
    assert abs(sum - 1) < 0.00001 

# The first 3 values in c must sum to 1
# The last value in d must be in the range [0...1]
def validate_d():
    global d
    sum = 0
    for di in d[0:3]:
        sum += di
    assert abs(sum - 1) < 0.00001 
    assert d[3] <= 1 and d[3] >= 0

# Validate all parameters of the fuzzing engine
def validate_all():
    validate_X()
    validate_b()
    validate_c()
    validate_d()
    validate_choose_mutation()
    validate_packet_selection_uniform_distribution()
    validate_fuzzing_state_uniform_distribution()
    validate_fuzzing_intensity()
    validate_construction_intensity()


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
    global FUZZING_INTENSITY, CONSTRUCTION_INTENSITY
    global b, c, d
    global X1, X2, X3

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

        elif arg[0] == 'PACKET_SELECTION_UNIFORM_DISTRIBUTION':
            PACKET_SELECTION_UNIFORM_DISTRIBUTION = int(arg[1])

        elif arg[0] == 'FUZZING_STATE_UNIFORM_DISTRIBUTION':
            FUZZING_STATE_UNIFORM_DISTRIBUTION = int(arg[1])

        elif arg[0] == 'FUZZING_INTENSITY':
            FUZZING_INTENSITY = float(arg[1])

        elif arg[0] == 'CONSTRUCTION_INTENSITY':
            CONSTRUCTION_INTENSITY = int(arg[1])

        elif arg[0] == 'X1':
            X1 = float(arg[1])
            user_supplied_X[0] = 1

        elif arg[0] == 'X2':
            X2 = float(arg[1])
            user_supplied_X[1] = 1

        elif arg[0] == 'X3':
            X3 = float(arg[1])
            user_supplied_X[2] = 1

        elif arg[0] == 'b':
            b = float(arg[1])

        elif arg[0][0] == 'c':
            # Assertion to make sure we give a proper ci key
            assert arg[0][1:] in [str(i) for i in range(1, 16)]
            index = int(arg[0][1:]) - 1
            c[index] = float(arg[1])

        elif arg[0][0] == 'd':
            # Assertion to make sure we give a proper di key
            assert arg[0][1:] in [str(i) for i in range(1, 5)]
            index = int(arg[0][1:]) - 1
            d[index] = float(arg[1])

# Print configuration parameters
def print_configuration():
    return ## TODO

def main():

    # Try to parse the supplied config file.
    # If one is not supplied, use the default values.
    try:
        config_f = open(sys.argv[1], 'r')
        config = config_f.readlines()
        parse_config_file(config)
        config_f.close()
    except FileNotFoundError:
        print("Could not find the supplied file: %s" % sys.argv[1])
        exit(-1)
    except IndexError:
        pass

    # Calculate X1, X2, and X3
    # calculate_X1()
    # calculate_X2()
    # calculate_X3()    

    validate_all()


if __name__ == "__main__":
    main()