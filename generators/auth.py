from connect import Connect
from packet import Packet
from packet import packetTest
from properties import Properties

class AuthVariableHeader(Packet):
    def __init__(self):
        super().__init__()

        self.reason_code = self.toBinaryData(None, 1, True)
        self.payload.append(self.reason_code)

        self.properties = Properties([0x15, 0x16, 0x1f, 0x26])
        self.payload.append(self.properties.toString())

class Auth(Packet):
    def __init__(self, protocol_version = None):
        super().__init__()

        self.fixed_header = "f0"
        self.variable_header = AuthVariableHeader()

        remaining_length = self.variable_header.getByteLength()

        self.payload = [self.fixed_header, self.toVariableByte("%x" % remaining_length), self.variable_header.toString()]


        
if __name__ == "__main__":
    packetTest([Connect, Auth], 300)