from parsers.parse_initializer import ParseInitializer
import helper_functions.determine_protocol_version as hpv
import globals as g

def handle_network_response(recv):
    print("Handling response: %s" % recv.hex())
    if len(recv) == 0:
        return

    if g.protocol_version == 0:
        g.protocol_version = hpv.determine_protocol_version(recv.hex())
    
    print("Using protocol version %d" % g.protocol_version)
    
    index = 0
    while index < len(recv.hex()):

        print("Handling payload: %s" % recv.hex()[index:])
        parser = ParseInitializer(recv.hex()[index:], g.protocol_version)
        
        print(parser.parser.G_fields)
        print(parser.parser.H_fields)
        index += parser.parser.index