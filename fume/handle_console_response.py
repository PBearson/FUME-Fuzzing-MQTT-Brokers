import globals as g
from difflib import SequenceMatcher
import helper_functions.print_verbosity as pv

def check_similarity(line):
    for response in g.console_response_log:
        similarity = SequenceMatcher(None, line, response).ratio()
        
        # If there is another response that is similar enough, then
        # we don't want the new response
        if similarity >= g.SIMILARITY_THRESHOLD:
            return True
    return False

# Handle responses from the target's console, AKA, stdout
# We listen for new messages, and when those messages are unique enough,
# we log them
def handle_console_response(proc):
    for line in iter(proc.stdout.readline, b''):

        # Ignore lines that we have seen already
        if line not in g.console_response_log:

            # Check the similarity between this line and others we have logged
            similarity = check_similarity(line)

            # If it is unique enough, log it
            # TODO we need a way to better check if we have just sent a payload to the target
            if similarity is False and type(g.payload) is bytearray:
                g.console_response_log[line] = g.payload
                pv.normal_print("Found new console response: " + line.decode("utf-8").strip())