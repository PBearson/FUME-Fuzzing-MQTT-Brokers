from packet import Packet
from packet import packetTest
from connect import Connect 
from properties import Properties
import random

class ConnackVariableHeader(Packet):
    def __init__(self, protocol_version):
        super().__init__()

        self.acknowledgement_flags = self.toBinaryData(None, 1, True, 1)
        self.payload.append(self.acknowledgement_flags)

        self.return_code = self.toBinaryData(None, 1, True)
        self.payload.append(self.return_code)

        self.connack_properties = Properties([0x11, 0x21, 0x24, 0x25, 0x27, 0x12, 0x22, 0x26, 0x28, 0x29, 0x21, 0x13, 0x1a, 0x1c, 0x15, 0x16])
        if protocol_version == 5:
            self.payload.append(self.connack_properties.toList())

class Connack(Packet):
    def __init__(self, protocol_version = None):
        super().__init__()

        if protocol_version is None:
            protocol_version = random.randint(3, 5)

        self.fixed_header = ['20']
        self.variable_header = ConnackVariableHeader(protocol_version)
        remaining_length = self.toVariableByte("%x" % self.variable_header.getByteLength())

        self.payload = [self.fixed_header, remaining_length, self.variable_header.toList()]

if __name__ == "__main__":
    packetTest([Connect, Connack], 300)