import sys
import random
import math
sys.path.append('generators')
sys.path.append('helper_functions')
sys.path.append('fume')

from generators.auth import Auth
import helper_functions.validate_fuzzing_params as vfp
import helper_functions.parse_config_file as pcf
import helper_functions.print_configuration as pc

import globals as g

import fume.markov_model as mm
import fume.fuzzing_engine as fe

# Calculate X1 from the construction intensity
def calculate_X1():
    g.X1 = 1 / g.CONSTRUCTION_INTENSITY

# Calculate X2 from the fuzzing intensity
def calculate_X2():
    g.X2 = 1 - g.FUZZING_INTENSITY

# Calculate X3 from the fuzzing intensity
def calculate_X3():
    g.X3 = 1 - (2 * math.log(1 + g.FUZZING_INTENSITY, 10))

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
    fe.run_fuzzing_engine(markov_model)

if __name__ == "__main__":
    main()