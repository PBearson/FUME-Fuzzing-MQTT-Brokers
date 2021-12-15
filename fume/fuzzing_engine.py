from generators.connect import Connect

import helper_functions.print_verbosity as pv
import globals as g
import random

# Convert a corpus (file) into a list of strings. Each element is 
# an MQTT packet.
def corpus_to_array(file):
    lines = file.readlines()
    for index, line in enumerate(lines):
        lines[index] = line.replace("\n", "")
    return lines

# Generate or seed a CONNECT packet
def handle_state_connect(mm):
    if mm.model_type == 'mutation':
        file = open("mqtt_corpus/CONNECT", "r")
        lines = corpus_to_array(file)
        payload = random.choice(lines)
        g.payload.append(payload)
        pv.debug_print("Payload so far: %s" % "".join(payload))
    else:
        g.payload.append(Connect())
        pv.debug_print("Payload so far: %s" % "".join([p.toString() for p in g.payload]))

# Handle the next state in the model
def handle_state(mm):
    state = mm.current_state.name

    # In state S0, reset the payload
    if state == 'S0':
        g.payload = []

    # In state RESPONSE_LOG, we select a payload from the previous responses
    # If the previous responses are empty, we just set the state to CONNECT
    elif state == 'RESPONSE_LOG':
        if len(g.network_response_log) > 0:
            g.payload += random.choice(g.network_response_log)
        else:
            mm.current_state = mm.state_connect
            handle_state(mm)

    elif state == 'CONNECT':
        handle_state_connect(mm)

# Run the fuzzing engine (indefinitely)
# mm: the markov model
def run_fuzzing_engine(mm):
    
    # Select model type
    model_types = ['mutation', 'generation']
    mm.model_type = random.choices(model_types, weights=[g.CHOOSE_MUTATION, 1 - g.CHOOSE_MUTATION])[0]
    pv.verbose_print("Selected model type %s" % mm.model_type)

    if mm.model_type == 'mutation':
        mm.state_s0.next = [mm.state_response_log, mm.state_connect]
        mm.state_s0.next_prob = [g.b, 1 - g.b]
    else:
        mm.state_s0.next = [mm.state_connect]
        mm.state_s0.next_prob = [1]

    while mm.current_state.name != 'Sf':
        pv.verbose_print("In state %s" % mm.current_state.name)
        handle_state(mm)
        mm.next_state()
