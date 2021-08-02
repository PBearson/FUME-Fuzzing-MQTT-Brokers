from connect import Connect
from packet import Packet
from packet import packetTest
from properties import Properties
import random

class SubscribePayload(Packet):
    def __init__(self, protocol_version):
        super().__init__()

        self.numTopics = random.randint(0, 10)

        for i in range(self.numTopics):
            topicLength = random.randint(0, 30)
            topic = self.toEncodedString(None, topicLength)
            self.payload.append(topic)

            topic_qos = random.randint(0, 2)
            no_local = random.randint(0, 1)
            retain_as_published = random.randint(0, 1)
            retain_handling = random.randint(0, 2)

            if protocol_version < 5:
                no_local = 0
                retain_as_published = 0
                retain_handling = 0
            
            subscription_options_tmp = [0b00, (retain_handling >> 1) & 1, retain_handling & 1, retain_as_published, no_local, (topic_qos >> 1) & 1, topic_qos & 1]

            subscription_options = ["%.2x" % int("".join(bin(s)[2:] for s in subscription_options_tmp), 2)]
            
            self.payload.append(subscription_options)

class SubscribeVariableHeader(Packet):
    def __init__(self, protocol_version):
        super().__init__()

        self.packet_identifier = self.toBinaryData(None, 2, True)
        self.payload.append(self.packet_identifier)

        self.properties = Properties([0x0b, 0x26])
        if protocol_version == 5:
            self.payload.append(self.properties.toString())

class Subscribe(Packet):
    def __init__(self, protocol_version = None):
        super().__init__()

        if protocol_version is None:
            protocol_version = random.randint(3, 5)

        self.fixed_header = "82"
        self.variable_header = SubscribeVariableHeader(protocol_version)
        self.subscribe_payload = SubscribePayload(protocol_version)

        remaining_length = self.variable_header.getByteLength() + self.subscribe_payload.getByteLength()

        self.payload = [self.fixed_header, self.toVariableByte("%x" % remaining_length), self.variable_header.toString(), self.subscribe_payload.toString()]
        
if __name__ == "__main__":
    packetTest([Connect, Subscribe], 300)