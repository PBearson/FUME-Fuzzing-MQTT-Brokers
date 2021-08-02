from connect import Connect
from packet import Packet
from packet import packetTest
from properties import Properties
import random

class PubackVariableHeader(Packet):
    def __init__(self, protocol_version):
        super().__init__()

        self.packet_identifier = self.toBinaryData(None, 2, True)
        self.payload.append(self.packet_identifier)

        self.reason_code = self.toBinaryData(None, 1, True)
        if protocol_version == 5:
            self.payload.append(self.reason_code)

        self.properties = Properties([0x1f, 0x26])
        if protocol_version == 5:
            self.payload.append(self.properties.toString())

class Puback(Packet):
    def __init__(self, protocol_version = None):
        super().__init__()
        
        if protocol_version is None:
            protocol_version = random.randint(3, 5)

        self.fixed_header = "40"
        self.variable_header = PubackVariableHeader(protocol_version)
        remaining_length = self.variable_header.getByteLength()

        self.payload = [self.fixed_header, self.toVariableByte("%x" % remaining_length), self.variable_header.toString()]

if __name__ == "__main__":
    packetTest([Connect, Puback], 300)