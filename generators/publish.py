from connect import Connect
from packet import Packet
from packet import packetTest
from properties import Properties
import random

class PublishFixedHeader(Packet):
    def __init__(self):
        super().__init__()

        self.dup = random.getrandbits(1)
        self.qos = min(2, random.getrandbits(2))
        self.retain = random.getrandbits(1)
        
        payload_tmp = [0b11, self.dup, (self.qos >> 1) & 1, self.qos & 1, self.retain]

        self.payload = ["%.2x" % int("".join(bin(s)[2:] for s in payload_tmp), 2)]

class PublishVariableHeader(Packet):
    def __init__(self, qos, protocol_version):
        super().__init__()

        self.topic_name_length = random.randint(0, 30)
        self.topic_name = self.toEncodedString(None, self.topic_name_length)
        self.payload.append(self.topic_name)

        self.packet_id = self.toBinaryData(None, 2, True, 8)
        if qos > 0:
            self.payload.append(self.packet_id)

        self.properties = Properties([0x01, 0x02, 0x23, 0x08, 0x09, 0x26, 0x0b, 0x03])
        if protocol_version == 5:
            self.payload.append(self.properties.toString())
    

class Publish(Packet):
    def __init__(self, protocol_version = None):
        super().__init__()

        if protocol_version is None:
            protocol_version = random.randint(3, 5)

        self.fixed_header = PublishFixedHeader()
        self.variable_header = PublishVariableHeader(self.fixed_header.qos, protocol_version)
        self.publish_message_length = random.randint(0, 100)
        self.publish_message = self.getAlphanumHexString(self.publish_message_length)

        remaining_length = self.variable_header.getByteLength() + self.publish_message_length
        self.payload = [self.fixed_header.toString(), self.toVariableByte("%x" % remaining_length), self.variable_header.toString(), self.publish_message]

if __name__ == "__main__":
    packetTest([Connect, Publish], 300)