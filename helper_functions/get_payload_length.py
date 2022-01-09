import globals as g

# Get the byte length of the payload, which might be
# represented as a list of strings, a bytearray, or a list of packet objects
def get_payload_length():
    if len(g.payload) == 0:
        return 0

    if type(g.payload) == bytearray:
        return len(g.payload)

    length = 0

    for p in g.payload:
        if type(g.payload[0]) == str:
            length += len(p)
        else:
            length += len(p.toString())

    return length / 2