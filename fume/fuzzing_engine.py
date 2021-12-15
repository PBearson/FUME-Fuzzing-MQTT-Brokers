import helper_functions.print_verbosity as pv
import globals as g
import random

def handle_state(mm):
    # TODO handle state depending on mutation or generation,
    # We may need to add a payload to the globals variable
    return

# Run the fuzzing engine (indefinitely)
# mm: the markov model
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

        handle_state(mm)
