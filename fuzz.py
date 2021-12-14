import sys
import random
import math
sys.path.append('generators')
sys.path.append('helper_functions')

from generators.auth import Auth
import helper_functions.validate_fuzzing_params as vfp
import helper_functions.parse_config_file as pcf
import helper_functions.print_configuration as pc

import globals as g

import markov_model as mm

import helper_functions.print_verbosity as pv

# Run the fuzzing engine (indefinitely)
def run_fuzzing_engine(mm):
    
    # Select model type
    model_types = ['mutation', 'generation']
    model_type = random.choices(model_types, weights=[g.CHOOSE_MUTATION, 1 - g.CHOOSE_MUTATION])[0]
    pv.verbose_print("Selected model type %s" % model_type)

    if model_type == 'mutation':
        mm.state_s0.next = [mm.state_response_log, mm.state_connect]
        mm.state_s0.next_prob = [g.b, 1 - g.b]
    else:
        mm.state_s0.next = [mm.state_connect]
        mm.state_s0.next_prob = [1]

    pv.verbose_print("In state %s" % mm.current_state.name)
    while mm.current_state.name != 'Sf':
        mm.next_state()
        pv.verbose_print("In state %s" % mm.current_state.name)

def RND(x):
    return round(x)

def RNG(x):
    return random.randint(0, x)

# Calculate X1 from the construction intensity
def calculate_X1():
    num = 1
    denom = 1 + RNG(RND(g.CONSTRUCTION_INTENSITY))
    g.X1 = num / denom

# Calculate X2 from the fuzzing intensity
def calculate_X2():
    num = 1
    denom = 1 + RNG(RND(100 * g.FUZZING_INTENSITY))
    g.X2 = num / denom

# Calculate X3 from the fuzzing intensity and construction intensity
def calculate_X3():
    fi = g.FUZZING_INTENSITY
    ci = g.CONSTRUCTION_INTENSITY
    num = 1
    denom = 1 + RNG(RND(math.log(1 + ci * fi)))
    g.X3 = num / denom

def main():
    # Try to parse the supplied config file.
    # If one is not supplied, use the default values.
    try:
        config_f = open(sys.argv[1], 'r')
        config = config_f.readlines()
        pcf.parse_config_file(config)
        config_f.close()
    except FileNotFoundError:
        print("Could not find the supplied file: %s" % sys.argv[1])
        exit(-1)
    except IndexError:
        pass

    # Calculate X1, X2, and X3 only if the user did not supply those values
    if g.user_supplied_X[0] == 0:
        calculate_X1()
    if g.user_supplied_X[1] == 0:
        calculate_X2()
    if g.user_supplied_X[2] == 0:
        calculate_X3()

    # Validate all parameters
    vfp.validate_all()

    # Print fuzzing configuration
    pc.print_configuration()

    # Initialize Markov Model
    markov_model = mm.initialize_markov_model()

    # Run the fuzzing loop
    run_fuzzing_engine(markov_model)

    

if __name__ == "__main__":
    main()