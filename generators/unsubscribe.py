from connect import Connect
from packet import Packet
from packet import packetTest
from properties import Properties
import random

class UnsubscribePayload(Packet):
    def __init__(self, protocol_version):
        super().__init__()

        self.numTopics = random.randint(0, 10)

        for i in range(self.numTopics):
            topicLength = random.randint(0, 30)
            topic = self.toEncodedString(None, topicLength)
            self.payload.append(topic)

class UnsubscribeVariableHeader(Packet):
    def __init__(self, protocol_version):
        super().__init__()

        self.packet_identifier = self.toBinaryData(None, 2, True)
        self.payload.append(self.packet_identifier)

        self.properties = Properties([0x26])
        if protocol_version == 5:
            self.payload.append(self.properties.toString())

class Unsubscribe(Packet):
    def __init__(self, protocol_version = None):
        super().__init__()

        if protocol_version is None:
            protocol_version = random.randint(3, 5)

        self.fixed_header = "a2"
        self.variable_header = UnsubscribeVariableHeader(protocol_version)
        self.unsubscribe_payload = UnsubscribePayload(protocol_version)

        remaining_length = self.variable_header.getByteLength() + self.unsubscribe_payload.getByteLength()

        self.payload = [self.fixed_header, self.toVariableByte("%x" % remaining_length), self.variable_header.toString(), self.unsubscribe_payload.toString()]
        
if __name__ == "__main__":
    packetTest([Connect, Unsubscribe], 300)