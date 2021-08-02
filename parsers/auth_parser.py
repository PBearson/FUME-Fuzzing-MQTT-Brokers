from protocol_parser import ProtocolParser as Parser
import sys
sys.path.append("generators")

from connect import Connect
from auth import Auth

from packet import sendToBroker

import random

class AuthParser(Parser):
    def __init__(self, payload, protocol_version):
        super().__init__(payload, protocol_version)

        self.index = self.insertByteNoIdentifier("reason code", payload, self.index, False)

        self.parseProperties()

def test():
    protocol_version = random.randint(3, 5)
    connect = Connect(protocol_version)
    payload = Auth(protocol_version)
    sendToBroker("localhost", 1883, connect.toString() + payload.toString())
    parser = AuthParser(payload.toString(), protocol_version)
    print(parser.G_fields)
    print(parser.H_fields)

if __name__ == "__main__":
    test()