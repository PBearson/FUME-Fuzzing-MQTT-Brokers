from protocol_parser import ProtocolParser as Parser
import sys
sys.path.append("generators")

from connect import Connect
from connack import Connack

from packet import sendToBroker

import random


class ConnackParser(Parser):
    def __init__(self, payload, protocol_version):
        super().__init__(payload, protocol_version)

        self.index = self.insertByteNoIdentifier("acknowledge flags", payload, self.index, True)

        self.index = self.insertByteNoIdentifier("reason code", payload, self.index, True)

        if protocol_version == 5:
            self.parseProperties()

def test():
    protocol_version = random.randint(3, 5)
    connect = Connect(protocol_version)
    payload = Connack(protocol_version)
    sendToBroker("localhost", 1883, connect.toString() + payload.toString())
    parser = ConnackParser(payload.toString(), protocol_version)
    print(parser.G_fields)
    print(parser.H_fields)

if __name__ == "__main__":
    test()