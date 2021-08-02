from packet import Packet
from packet import packetTest
from connect import Connect
from properties import Properties
import random

class DisconnectVariableHeader(Packet):
    def __init__(self, protocol_version):
        super().__init__()

        self.reason_code = self.toBinaryData(None, 1, True)
        if protocol_version == 5:
            self.payload.append(self.reason_code)

        self.properties = Properties([0x11, 0x1f, 0x26, 0x1c])
        if protocol_version == 5:
            self.payload.append(self.properties.toString())
    

class Disconnect(Packet):
    def __init__(self, protocol_version = None):
        super().__init__()

        if protocol_version is None:
            protocol_version = random.randint(3, 5)

        self.fixed_header = ['e0']
        self.variable_header = DisconnectVariableHeader(protocol_version)

        remaining_length = self.variable_header.getByteLength()

        self.payload = [self.fixed_header, self.toVariableByte("%x" % remaining_length), self.variable_header.toString()]

if __name__ == "__main__":
    packetTest([Connect, Disconnect], 250)