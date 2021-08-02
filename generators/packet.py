import socket
import string
import random
import math
import time

class Packet:
    def __init__(self):
        self.payload = []

    def toList(self):
        l = []
        for p in self.payload:
            for n in p:
                if type(n) == list:
                    for x in n:
                        l.append(x)
                else:
                    l.append(n)
        return l
        
    def toString(self):
        return "".join(self.toList())

    def getByteLength(self):
        lenFloat = len(self.toString()) / 2
        assert math.ceil(lenFloat) == math.floor(lenFloat)
        return int(lenFloat)

    def toVariableByte(self, byteString):
        varByte = ""
        byteInt = int(byteString, 16)
        while True:
            encoded = int(byteInt % 128)
            byteInt = int(byteInt / 128)
            if byteInt > 0:
                encoded = encoded | 128

            varByte += "%.2x" % encoded
            if byteInt <= 0:
                break

        return varByte

    # Calculate the length of the payload and add it to the beginning 
    # of the payload.
    def prependPayloadLength(self):
        payload_length = self.toVariableByte("%x" % (self.getByteLength()))
        self.payload.insert(0, payload_length)

    def getAlphanumHexString(self, stringLength, userstring = None):
        if userstring is not None:
            return ["%.2x" % ord(s) for s in userstring]

        alphanum = string.ascii_letters + string.digits
        return ["%.2x" % ord(random.choice(alphanum)) for i in range(stringLength)]

    # identifier: a 1-byte integer (may be null)
    # stringLength: a 2-byte integer
    # userstring: an optional user-defined string. If not defined, the string is random.
    # Return: an encoding in the format [ID, Len, String] or [Len, String]
    def toEncodedString(self, identifier, stringLength, userstring = None):
        if userstring is None:
            userstring = self.getAlphanumHexString(stringLength)
        else:
            userstring = self.getAlphanumHexString(stringLength, userstring)
        if identifier is None:
            return ["%.4x" % len(userstring), userstring]
        return ["%.2x" % identifier, "%.4x" % len(userstring), userstring]

    # identifier: a 1-byte integer
    # string1Length/string2Length: 2-byte integers
    # Return: an encoding in the format [ID, Len1, String1, Len2, String2]
    def toEncodedStringPair(self, identifier, string1Length, string2Length):
        return ["%.2x" % identifier, "%.4x" % string1Length, self.getAlphanumHexString(string1Length), "%.4x" % string2Length, self.getAlphanumHexString(string2Length)]

    # identifier: a 1-byte integer (may be null)
    # byteLength: a 2-byte integer
    # omitLength: bool, means the byte length field is excluded
    # maxBits: an integer in the range [0-8]. Dictates the max number of 1-bits per byte.
    # minBits: an integer in the range [0-255]. Dictates the maximum possible size per byte.
    # Return: a binary encoding in one of the following formats:
    #   - [ID, Len, Bytes]
    #   - [ID, Bytes]
    #   - [Len, Bytes]
    #   - [Bytes]
    def toBinaryData(self, identifier, byteLength, omitLength = False, maxBits = 8, minValue = 0):
        
        if identifier is None:
            fullData = ["%.4x" % byteLength, ["%.2x" % max(minValue, random.getrandbits(maxBits)) for i in range(byteLength)]]
            if omitLength:
                return fullData[1]
            else:
                return fullData
        else:
            fullData = ["%.2x" % identifier, "%.4x" % byteLength, ["%.2x" % max(minValue, random.getrandbits(maxBits)) for i in range(byteLength)]]
            if omitLength:
                return [fullData[0], fullData[2]]
            else:
                return fullData

    # Append the payload with newPacket 50% of the time
    def appendPayloadRandomly(self, newPacket):
        if random.getrandbits(1) == 0:
            self.payload.append(newPacket)

# Send a payload to a broker.
def sendToBroker(host, port, payload, silenceError = False, killOnError = True):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
        if type(payload) == str:
            s.send(bytearray.fromhex(payload))
        else:
            s.send(payload)
    except ValueError:
        if not silenceError:
            print("ValueError caused by following payload:")
            print(payload)
        if killOnError:
            exit(0)
    except ConnectionRefusedError:
        if not silenceError:
            print("ConnectRefusedError caused by following payload:")
            print(payload)
        if killOnError:
            exit(0)
    except ConnectionResetError:
        pass
    s.close()

def packetTest(packetTypes, runs = 10, verbose = False):
    host = "127.0.0.1"
    port = 1883

    for i in range(runs):
        payload = ""
        protocol_version = random.randint(3, 5)
        for p in packetTypes:
            payload += p(protocol_version).toString()
        if verbose:
            print("Sending payload: ", payload)
        sendToBroker(host, port, payload)
        time.sleep(0.01)