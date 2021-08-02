from protocol_parser import ProtocolParser as Parser
import sys
sys.path.append("generators")

from connect import Connect
from pubcomp import Pubcomp

from packet import sendToBroker

import random

class PubcompParser(Parser):
    def __init__(self, payload, protocol_version):
        super().__init__(payload, protocol_version)

        self.index = self.insertTwoBytesNoIdentifier("packet identifier", payload, self.index, False)

        if protocol_version == 5:
            self.index = self.insertByteNoIdentifier("reason code", payload, self.index, True)

            self.parseProperties()

def test():
    protocol_version = random.randint(3, 5)
    connect = Connect(protocol_version)
    payload = Pubcomp(protocol_version)
    sendToBroker("localhost", 1883, connect.toString() + payload.toString())
    parser = PubcompParser(payload.toString(), protocol_version)
    print(parser.G_fields)
    print(parser.H_fields)

if __name__ == "__main__":
    test()