import random
import binascii
import string

from packet import Packet
from packet import packetTest
from properties import Properties
        
class ConnectFlags(Packet):
    def __init__(self):        
        self.username_flag = random.getrandbits(1)
        self.password_flag = random.getrandbits(1)
        self.will_retain = random.getrandbits(1)
        self.will_qos = min(2, random.getrandbits(2))
        self.will_flag = random.getrandbits(1)
        self.clean_start = random.getrandbits(1)
        self.reserved = 0
        
        if self.will_flag == 0:
            self.will_qos = 0

        if self.will_flag == 0:
            self.will_retain = 0

        payload_tmp = [self.username_flag, self.password_flag, self.will_retain, self.will_qos & 1, (self.will_qos >> 1) & 1, self.will_flag, self.clean_start, self.reserved]

        self.payload = ["%.2x" % int("".join(bin(s)[2:] for s in payload_tmp), 2)]

class ConnectVariableHeader(Packet):
    def __init__(self, protocol_version):
        if protocol_version == 3:
            self.name = self.toEncodedString(None, 6, "MQIsdp")
        else:
            self.name = self.toEncodedString(None, 4, "MQTT")
        self.protocol_version = ["%.2x" % protocol_version]
        self.flags = ConnectFlags()
        self.keepalive = self.toBinaryData(None, 2, True)
        self.properties = Properties([0x11, 0x21, 0x27, 0x22, 0x19, 0x17, 0x26, 0x15, 0x16])

        self.payload = [self.name, self.protocol_version, self.flags.toList(), self.keepalive]

        if protocol_version == 5:
            self.payload.append(self.properties.toList())

class ConnectPayload(Packet):
    def __init__(self, header):
        self.clientid_len = random.randint(0, 30)
        self.clientid = self.toEncodedString(None, self.clientid_len)
        self.will_properties = Properties([0x18, 0x01, 0x02, 0x03, 0x08, 0x09, 0x26])
        self.will_topic_length = random.randint(0, 30)
        self.will_topic = self.toEncodedString(None, self.will_topic_length)
        self.will_payload_length = random.randint(0, 30)
        self.will_payload = self.toEncodedString(None, self.will_payload_length)
        self.username_length = random.randint(0, 30)
        self.username = self.toEncodedString(None, self.username_length)
        self.password_length = random.randint(0, 30)
        self.password = self.toEncodedString(None, self.password_length)

        self.payload = [self.clientid]

        if header.flags.will_flag == 1:
            if int(header.protocol_version[0]) == 5:
                self.payload.append(self.will_properties.toList())

            self.payload.append(self.will_topic)
            self.payload.append(self.will_payload)
            
        if header.flags.username_flag == 1:
            self.payload.append(self.username)
        
        if header.flags.password_flag == 1:
            self.payload.append(self.password)

class Connect(Packet):
    def __init__(self, protocol_version = None):
        super().__init__()

        if protocol_version is None:
            protocol_version = random.randint(3, 5)

        self.fixed_header = ["%.2x" % 0b10000]
        self.variable_header = ConnectVariableHeader(protocol_version)
        self.connect_payload = ConnectPayload(self.variable_header)

        remaining_length = self.variable_header.getByteLength() + self.connect_payload.getByteLength()
        
        self.payload = [self.fixed_header, self.toVariableByte("%x" % remaining_length), self.variable_header.toList(), self.connect_payload.toList()]

if __name__ == "__main__":
    packetTest([Connect], 10)