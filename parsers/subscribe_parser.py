from protocol_parser import ProtocolParser as Parser
import sys
sys.path.append("generators")

from connect import Connect
from subscribe import Subscribe

from packet import sendToBroker

import random

class SubscribeParser(Parser):
    def __init__(self, payload, protocol_version):
        super().__init__(payload, protocol_version)

        self.index = self.insertTwoBytesNoIdentifier("packet identifier", payload, self.index, False)

        if protocol_version == 5:
            self.parseProperties()

        while self.index < len(payload):
            self.index = self.insertStringListNoIdentifier("topic", payload, self.index, False)
            self.index = self.insertByteListNoIdentifier("subscription options", payload, self.index, True)

def test():
    protocol_version = random.randint(3, 5)
    connect = Connect(protocol_version)
    payload = Subscribe(protocol_version)
    sendToBroker("localhost", 1883, connect.toString() + payload.toString())
    parser = SubscribeParser(payload.toString(), protocol_version)
    print(parser.G_fields)
    print(parser.H_fields)

if __name__ == "__main__":
    test()