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

if __name__ == "__main__":
    payload = "312d0023245359532f62726f6b65722f6c6f61642f7075626c6973682f73656e742f31356d696e31363233372e373831"
    index = 0
    while index < len(payload):
        try:
            parser = ParseInitializer(payload[index:], 3)        
            print(parser.parser.G_fields)
            print(parser.parser.H_fields)
            index +=  2 * (parser.parser.remainingLengthToInteger()) + 2 + len(parser.parser.remaining_length)

        # If the parser throws a ValueError, chances are that the payload
        # is malformed. In that case, we skip the current byte and hope for 
        # the best.
        except ValueError:
            index += 2