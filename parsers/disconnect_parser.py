from protocol_parser import ProtocolParser as Parser
import sys
sys.path.append("generators")

from connect import Connect
from disconnect import Disconnect

from packet import sendToBroker

import random

class DisconnectParser(Parser):

    def __init__(self, payload, protocol_version):
        super().__init__(payload, protocol_version)

        if protocol_version == 5:
            self.index = self.insertByteNoIdentifier("reason code", payload, self.index, True)

        if protocol_version == 5:
            self.parseProperties()

def test():
    protocol_version = random.randint(3, 5)
    connect = Connect(protocol_version)
    payload = Disconnect(protocol_version)
    sendToBroker("localhost", 1883, connect.toString() + payload.toString())
    parser = DisconnectParser(payload.toString(), protocol_version)
    print(parser.G_fields)
    print(parser.H_fields)

if __name__ == "__main__":
    test()