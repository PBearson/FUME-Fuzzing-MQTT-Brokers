from protocol_parser import ProtocolParser as Parser
import sys
sys.path.append("generators")

from connect import Connect
from publish import Publish

from packet import sendToBroker

import random

class PublishParser(Parser):

    # Given the fixed header, return the QoS version, defined by bits 1 and 2.
    def getQoSVersion(self, fixed_header):
        return int(bin(fixed_header)[-3:-1], 2)

    def __init__(self, payload, protocol_version):
        super().__init__(payload, protocol_version)

        self.index = self.insertStringNoIdentifier("topic name", payload, self.index, False)

        fixed_header = int(self.G_fields["fixed header"], 16)
        if self.getQoSVersion(fixed_header) > 0:
            self.index = self.insertTwoBytesNoIdentifier("packet identifier", payload, self.index, False)

        if protocol_version == 5:
            self.parseProperties()

        self.H_fields["message"] = payload[self.index:]


def test():
    protocol_version = random.randint(3, 5)
    connect = Connect(protocol_version)
    payload = Publish(protocol_version)
    sendToBroker("localhost", 1883, connect.toString() + payload.toString())
    parser = PublishParser(payload.toString(), protocol_version)
    print(parser.G_fields)
    print(parser.H_fields)

if __name__ == "__main__":
    test()