from generators.connect import Connect
from generators.connack import Connack
from generators.publish import Publish
from generators.puback import Puback
from generators.pubrec import Pubrec
from generators.pubrel import Pubrel
from generators.pubcomp import Pubcomp
from generators.subscribe import Subscribe
from generators.suback import Suback
from generators.unsubscribe import Unsubscribe
from generators.unsuback import Unsuback
from generators.pingreq import Pingreq
from generators.pingresp import Pingresp
from generators.disconnect import Disconnect
from generators.auth import Auth

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

def handle_select_or_generation_state(mm, packet):
    state_name = mm.current_state.name

    if mm.model_type == 'mutation':
        file = open("mqtt_corpus/" + state_name, "r")
        lines = corpus_to_array(file)
        payload = random.choice(lines)
        g.payload.append(payload)
        pv.debug_print("Added payload %s" % payload)
        pv.debug_print("Payload so far: %s" % "".join(g.payload))
    else:
        payload = packet()
        g.payload.append(payload)
        pv.debug_print("Added payload %s" % payload.toString())
        pv.debug_print("Payload so far: %s" % "".join([p.toString() for p in g.payload]))
    
# Handle the next state in the model
def handle_state(mm):
    state = mm.current_state.name

    # In state S0, reset the payload
    if state == 'S0':
        g.payload = []

    # In state RESPONSE_LOG, we select a payload from the previous responses. If the previous responses are empty, we just set 
    # the state to CONNECT
    elif state == 'RESPONSE_LOG':
        if len(g.network_response_log) > 0:
            g.payload += random.choice(g.network_response_log)
        else:
            mm.current_state = mm.state_connect
            handle_state(mm)

    # For the packet-specific states, we either connect or generate
    # the desired packet and append it to the payload

    elif state == 'CONNECT':
        handle_select_or_generation_state(mm, Connect)

    elif state == 'CONNACK':
        handle_select_or_generation_state(mm, Connack)

    elif state == 'PUBLISH':
        handle_select_or_generation_state(mm, Publish)

    elif state == 'PUBACK':
        handle_select_or_generation_state(mm, Puback)
    
    elif state == 'PUBREC':
        handle_select_or_generation_state(mm, Pubrec)

    elif state == 'PUBREL':
        handle_select_or_generation_state(mm, Pubrel)

    elif state == 'PUBCOMP':
        handle_select_or_generation_state(mm, Pubcomp)

    elif state == 'SUBSCRIBE':
        handle_select_or_generation_state(mm, Subscribe)

    elif state == 'SUBACK':
        handle_select_or_generation_state(mm, Suback)

    elif state == 'UNSUBSCRIBE':
        handle_select_or_generation_state(mm, Unsubscribe)

    elif state == 'UNSUBACK':
        handle_select_or_generation_state(mm, Unsuback)

    elif state == 'PINGREQ':
        handle_select_or_generation_state(mm, Pingreq)
    
    elif state == 'PINGRESP':
        handle_select_or_generation_state(mm, Pingresp)

    elif state == 'DISCONNECT':
        handle_select_or_generation_state(mm, Disconnect)

    elif state == 'AUTH':
        handle_select_or_generation_state(mm, Auth)



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
