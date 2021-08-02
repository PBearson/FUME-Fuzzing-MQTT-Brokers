from protocol_parser import ProtocolParser as Parser
import sys
sys.path.append("generators")

from connect import Connect
from pingreq import Pingreq

from packet import sendToBroker

import random

class PingreqParser(Parser):
    def __init__(self, payload, protocol_version):
        super().__init__(payload, protocol_version)

def test():
    protocol_version = random.randint(3, 5)
    connect = Connect(protocol_version)
    payload = Pingreq(protocol_version)
    sendToBroker("localhost", 1883, connect.toString() + payload.toString())
    parser = PingreqParser(payload.toString(), protocol_version)
    print(parser.G_fields)
    print(parser.H_fields)

if __name__ == "__main__":
    test()