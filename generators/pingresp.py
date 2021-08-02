from connect import Connect
from packet import Packet
from packet import packetTest

class Pingresp(Packet):
    def __init__(self, protocol_version = None):
        super().__init__()

        self.payload = "d000"
        
if __name__ == "__main__":
    packetTest([Connect, Pingresp], 300)