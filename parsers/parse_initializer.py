# This file will receive the payload and decide which parser to pass it to, 
# based on the first byte in the fixed header.

from protocol_parser import ProtocolParser
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
            try:
                self.parser = packetDict[payload[0]](payload, protocol_version)

            # KeyError means that the payload is not a valid MQTT packet, so we create 
            # a "fake" Parser object (from an empty string a protocol version 0)
            except KeyError:
                self.parser = ProtocolParser("", 0)
        else:
            self.parser = None

if __name__ == "__main__":
    payload = "200200003b0a0001350001494a6a44393b0a0001350002494a6a44393b0a0001350003494a6a44393b0a0001350004494a6a44393b0a0001350005494a6a44393b0a0001350006494a6a44393a1c00013500074832417a43317238506876645748764d7559714643636d3b0a0001350008494a6a44393b0a0001350009494a6a44393b0a000135000a494a6a44393b0a000135000b494a6a44393b0a000135000c494a6a44393b0a000135000d494a6a44393b0a000135000e494a6a44393b0a000135000f494a6a44393b0a0001350010494a6a44393b0a0001350011494a6a44393b0a0001350012494a6a44393b0a0001350013494a6a44393a080001350014776f593b0a0001350015494a6a44393b0a0001350016494a6a44393b0a0001350017494a6a44393b0a0001350018494a6a44393b0a0001350019494a6a44393b0a000135001a494a6a44393b0a000135001b494a6a44393b0a000135001c494a6a44393b0a000135001d494a6a44393b0f000135001f69516a765674446e4a533b0f000135002069516a765674446e4a533b0800013500225372743b0800013500245372743b0800013500255372743b0800013500265372743b0800013500285372743b0800013500295372743b08000135002a5372743b08000135002b5372743b08000135002c5372743b08000135002d5372743b08000135002e5372743b08000135002f5372743b0800013500305372743b0800013500315372743b0800013500325372743b0800013500335372743b0800013500345372743b0800013500355372743b0800013500365372743b0800013500375372743b0800013500385372743b0800013500395372743b08000135003a5372743b08000135003b5372743b08000135003c5372743b08000135003d5372743b08000135003e5372743b08000135003f5372743b0800013500405372743b0800013500415372743b0800013500425372743b0800013500435372743b0800013500445372743b0800013500455372743b0800013500465372743b0800013500475372743b0800013500485372743b0800013500495372743b08000135004a5372743b08000135004b5372743b08000135004c5372743b08000135004d5372743b08000135004e5372743b08000135004f5372743b0800013500505372743b0800013500515372743b0800013500525372743b0800013500535372743b0800013500545372743b0800013500555372743b0800013500565372743b0800013500585372743b0800013500595372743b08000135005a5372743b08000135005b5372743b08000135005c5372743b08000135005d5372743b08000135005e5372743b08000135005f5372743b0800013500605372743b0800013500615372743b0800013500625372743b11"
    index = 0
    while index < len(payload):
        try:
            print("Remaining payload: %s" % payload[index:])
            parser = ParseInitializer(payload[index:], 3)        
            print(parser.parser.G_fields)
            print(parser.parser.H_fields)
            index +=  2 * (parser.parser.remainingLengthToInteger()) + 2 + len(parser.parser.remaining_length)

        # If the parser throws a ValueError, chances are that the payload
        # is malformed. In that case, we skip the current byte and hope for 
        # the best.
        except ValueError:
            index += 2