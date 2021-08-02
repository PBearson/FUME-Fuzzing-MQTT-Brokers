from connect import Connect
from packet import Packet
from packet import packetTest
from properties import Properties
import random

class SubackPayload(Packet):
    def __init__(self, protocol_version):
        super().__init__()

        self.numReasonCodes = random.randint(0, 10)

        for i in range(self.numReasonCodes):
            reasonCode = self.toBinaryData(None, 1, True)
            self.payload.append(reasonCode)

class SubackVariableHeader(Packet):
    def __init__(self, protocol_version):
        super().__init__()

        self.packet_identifier = self.toBinaryData(None, 2, True)
        self.payload.append(self.packet_identifier)

        self.properties = Properties([0x1f, 0x26])
        if protocol_version == 5:
            self.payload.append(self.properties.toString())

class Suback(Packet):
    def __init__(self, protocol_version = None):
        super().__init__()

        if protocol_version is None:
            protocol_version = random.randint(3, 5)

        self.fixed_header = "90"
        self.variable_header = SubackVariableHeader(protocol_version)
        self.suback_payload = SubackPayload(protocol_version)

        remaining_length = self.variable_header.getByteLength() + self.suback_payload.getByteLength()

        self.payload = [self.fixed_header, self.toVariableByte("%x" % remaining_length), self.variable_header.toString(), self.suback_payload.toString()]
        
if __name__ == "__main__":
    packetTest([Connect, Suback], 300)