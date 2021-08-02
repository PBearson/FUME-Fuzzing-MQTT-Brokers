from protocol_parser import ProtocolParser as Parser
import sys
sys.path.append("generators")

from connect import Connect
from suback import Suback

from packet import sendToBroker

import random

class SubackParser(Parser):
    def __init__(self, payload, protocol_version):
        super().__init__(payload, protocol_version)

        self.index = self.insertTwoBytesNoIdentifier("packet identifier", payload, self.index, False)

        if protocol_version == 5:
            self.parseProperties()

        while self.index < len(payload):
            self.index = self.insertByteListNoIdentifier("return code", payload, self.index, True)

def test():
    protocol_version = random.randint(3, 5)
    connect = Connect(protocol_version)
    payload = Suback(protocol_version)
    sendToBroker("localhost", 1883, connect.toString() + payload.toString())
    parser = SubackParser(payload.toString(), protocol_version)
    print(parser.G_fields)
    print(parser.H_fields)

if __name__ == "__main__":
    test()