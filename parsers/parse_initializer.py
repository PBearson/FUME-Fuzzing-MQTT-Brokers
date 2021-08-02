# This file will receive the payload and decide which parser to pass it to, 
# based on the first byte in the fixed header.

from connack_parser import ConnackParser
from publish_parser import PublishParser
from disconnect_parser import DisconnectParser
from puback_parser import PubackParser
from pubrec_parser import PubrecParser
from pubrel_parser import PubrelParser
from pubcomp_parser import PubcompParser
from subscribe_parser import SubscribeParser
from suback_parser import SubackParser
from unsubscribe_parser import UnsubscribeParser
from unsuback_parser import UnsubackParser
from pingreq_parser import PingreqParser
from pingresp_parser import PingrespParser
from auth_parser import AuthParser

class ParseInitializer:
    def __init__(self, payload, protocol_version):
        assert type(payload) == str
        packetDict = {
            '2': ConnackParser, 
            '3': PublishParser,
            '4': PubackParser,
            '5': PubrecParser,
            '6': PubrelParser,
            '7': PubcompParser,
            '8': SubscribeParser,
            '9': SubackParser,
            'a': UnsubscribeParser,
            'b': UnsubackParser,
            'c': PingreqParser,
            'd': PingrespParser,
            'e': DisconnectParser,
            'f': AuthParser}

        if len(payload) > 0:
            self.parser = packetDict[payload[0]](payload, protocol_version)
        else:
            self.parser = None