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

# In state S2, convert the payload to a string (unless we have 
# already done so)
def handle_s2_state(mm):
    if type(g.payload) is str:
        return

    if mm.model_type == 'mutation':
        g.payload = "".join(g.payload)
    else:
        g.payload = "".join([p.toString() for p in g.payload])

# Inject many bytes into the payload
# Default behavior is to inject between 1 and 10 times the length
# of the payload, up to a defined maximum payload length 
def handle_bof_state():
    if len(g.payload) >= 10000:
        return

    minlen = (1 + g.FUZZING_INTENSITY) * len(g.payload)
    maxlen = 5 * (1 + g.FUZZING_INTENSITY) * len(g.payload)
    inject_len = random.randint(round(minlen), round(maxlen))
    inject_payload = str(random.getrandbits(inject_len * 8))
    
    for p in inject_payload:
        index = random.randint(0, len(g.payload))
        g.payload = g.payload[:index] + p + g.payload[index:] 

    pv.debug_print("Fuzzed payload now (injected %d bytes): %s" % (inject_len, g.payload))

# Inject some bytes into the payload
def handle_nonbof_state():
    if len(g.payload) >= 10000:
        return

    maxlen = len(g.payload) * g.FUZZING_INTENSITY
    inject_len = random.randint(1, round(maxlen))
    inject_payload = str(random.getrandbits(inject_len * 8))

    for p in inject_payload:
        index = random.randint(0, len(g.payload))
        g.payload = g.payload[:index] + p + g.payload[index:] 

    pv.debug_print("Fuzzed payload now (injected %d bytes): %s" % (inject_len, g.payload))

# Remove some bytes from the payload
def handle_delete_state():
    if len(g.payload) <= 2:
        return

    maxlen = len(g.payload) * g.FUZZING_INTENSITY
    delete_len = random.randint(1, round(maxlen))

    for d in range(delete_len):
        index = random.randint(0, len(g.payload))
        g.payload = g.payload[:index] + g.payload[index + 1:]

    pv.debug_print("Fuzzed payload now (deleted %d bytes): %s" % (delete_len, g.payload))

# Mutate some bytes in the payload
def handle_mutate_state():
    maxlen = len(g.payload) * g.FUZZING_INTENSITY
    mutate_len = random.randint(1, round(maxlen))
    mutate_payload = str(random.getrandbits(mutate_len * 8))

    for p in mutate_payload:
        index = random.randint(0, len(g.payload))
        g.payload = g.payload[:index] + p + g.payload[index + 1:] 

    pv.debug_print("Fuzzed payload now (mutated %d bytes): %s" % (mutate_len, g.payload))

# Either select (from the corpus) or generate a new packet
# and append it the payload
# mm: the markov model
# packet: a Packet class 
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
        if len(g.payload) == 0:
            payload = packet()
        else:
            protocol_version = g.payload[0].protocol_version
            payload = packet(protocol_version)
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

    elif state == 'S2':
        handle_s2_state(mm)

    # In states S1, INJECT, and Sf, we just proceed to the next state
    elif state in ['S1', 'INJECT', 'Sf']:
        return

    # In state BOF, we inject many, many bytes into the payload
    elif state == 'BOF':
        handle_bof_state()

    # In state BOF, we inject a few bytes into the payload
    elif state == 'NONBOF':
        handle_nonbof_state()

    # In state DELETE, we delete a few bytes from the payload
    elif state == 'DELETE':
        handle_delete_state()

    # In state MUTATE, we mutate a few bytes in the payload
    elif state == 'MUTATE':
        handle_mutate_state()


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

    while True:
        mm.current_state = mm.state_s0
        while mm.current_state.name != 'Sf':
            pv.verbose_print("In state %s" % mm.current_state.name)
            handle_state(mm)
            mm.next_state()
        break