import globals as g
import random

class Node():
    def __init__(self, name):
        self.name = name
        self.next = []
        self.next_prob = []

class Markov_Model():
    def __init__(self):
        self.state_s0 = Node('S0')
        self.state_s1 = Node("S1")
        self.state_s2 = Node('S2')
        self.state_sf = Node('Sf')
        self.state_inject = Node('INJECT')
        self.state_delete = Node('DELETE')
        self.state_mutate = Node('MUTATE')
        self.state_bof = Node('BOF')
        self.state_nonbof = Node('NONBOF')
        self.state_send = Node('SEND')
        self.state_response_log = Node('RESPONSE_LOG')
        self.state_connect = Node("CONNECT")
        self.state_connack = Node("CONNACK")
        self.state_publish = Node("CONNACK")
        self.state_puback = Node("PUBACK")
        self.state_pubrec = Node("PUBREC")
        self.state_pubrel = Node("PUBREL")
        self.state_pubcomp = Node("PUBCOMP")
        self.state_subscribe = Node("SUBSCRIBE")
        self.state_suback = Node("SUBACK")
        self.state_unsubscribe = Node("UNSUBSCRIBE")
        self.state_unsuback = Node("UNSUBACK")
        self.state_pingreq = Node("PINGREQ")
        self.state_pingresp = Node("PINGRESP")
        self.state_disconnect = Node("DISCONNECT")
        self.state_auth = Node("AUTH")

        self.current_state = self.state_s0

        self.model_type = 'mutation'

    # Proceed to the next state in the Markov chain
    def next_state(self):
        if self.current_state.name == 'Sf':
            return 
            
        self.current_state = random.choices(
            self.current_state.next, 
            weights=self.current_state.next_prob)[0]

def initialize_markov_model():
    mm = Markov_Model()

    # S0 - by default, we assume mutation model.
    mm.state_s0.next = [mm.state_response_log, mm.state_connect]
    mm.state_s0.next_prob = [g.b, 1 - g.b]

    # Response log
    mm.state_response_log.next = [mm.state_s2]
    mm.state_response_log.next_prob = [1]

    # S1
    mm.state_s1.next = [
        mm.state_connect, 
        mm.state_connack, 
        mm.state_publish, 
        mm.state_puback,
        mm.state_pubrec,
        mm.state_pubrel,
        mm.state_pubcomp,
        mm.state_subscribe,
        mm.state_suback,
        mm.state_unsubscribe,
        mm.state_suback,
        mm.state_pingreq,
        mm.state_pingresp,
        mm.state_disconnect,
        mm.state_auth,
        mm.state_s2]

    for ci in g.c:
        mm.state_s1.next_prob.append(ci - (ci * g.X1))
    mm.state_s1.next_prob.append(g.X1)

    # Connect
    mm.state_connect.next = [mm.state_s1]
    mm.state_connect.next_prob = [1]

    # Connack
    mm.state_connack.next = [mm.state_s1]
    mm.state_connack.next_prob = [1]

    # Publish
    mm.state_publish.next = [mm.state_s1]
    mm.state_publish.next_prob = [1]

    # Puback
    mm.state_puback.next = [mm.state_s1]
    mm.state_puback.next_prob = [1]

    # Pubrec
    mm.state_pubrec.next = [mm.state_s1]
    mm.state_pubrec.next_prob = [1]

    # Pubrel
    mm.state_pubrel.next = [mm.state_s1]
    mm.state_pubrel.next_prob = [1]

    # Pubcomp
    mm.state_pubcomp.next = [mm.state_s1]
    mm.state_pubcomp.next_prob = [1]

    # Subscribe
    mm.state_subscribe.next = [mm.state_s1]
    mm.state_subscribe.next_prob = [1]

    # Suback
    mm.state_suback.next = [mm.state_s1]
    mm.state_suback.next_prob = [1]

    # Unsubscribe
    mm.state_unsubscribe.next = [mm.state_s1]
    mm.state_unsubscribe.next_prob = [1]

    # Unsuback
    mm.state_unsuback.next = [mm.state_s1]
    mm.state_unsuback.next_prob = [1]

    # Pingreq
    mm.state_pingreq.next = [mm.state_s1]
    mm.state_pingreq.next_prob = [1]

    # Pingresp
    mm.state_pingresp.next = [mm.state_s1]
    mm.state_pingresp.next_prob = [1]

    # Disconnect
    mm.state_disconnect.next = [mm.state_s1]
    mm.state_disconnect.next_prob = [1]

    # Auth
    mm.state_auth.next = [mm.state_s1]
    mm.state_auth.next_prob = [1]

    # S2
    mm.state_s2.next = [
        mm.state_inject,
        mm.state_delete,
        mm.state_mutate,
        mm.state_send
    ]
    for di in g.d[:3]:
        mm.state_s2.next_prob.append(di - (di * g.X2))
    mm.state_s2.next_prob.append(g.X2)

    # Inject
    mm.state_inject.next = [mm.state_bof, mm.state_nonbof]
    mm.state_inject.next_prob = [g.d[3], 1 - g.d[3]]

    # Delete
    mm.state_delete.next = [mm.state_s2]
    mm.state_delete.next_prob = [1]

    # Mutate
    mm.state_mutate.next = [mm.state_s2]
    mm.state_mutate.next_prob = [1]

    # BOF
    mm.state_bof.next = [mm.state_s2]
    mm.state_bof.next_prob = [1]

    # Non-BOF
    mm.state_nonbof.next = [mm.state_s2]
    mm.state_nonbof.next_prob = [1]

    # Send
    mm.state_send.next = [mm.state_s2, mm.state_sf]
    mm.state_send.next_prob = [1 - g.X3, g.X3]

    return mm