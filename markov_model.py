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

def initialize_markov_model():
    markov_model = Markov_Model()

    return markov_model