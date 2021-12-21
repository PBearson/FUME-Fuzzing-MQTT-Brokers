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

def handle_console_response(proc):
    for line in iter(proc.stdout.readline, b''):
        # TODO add similarity threshold to config file
        # TODO log line if it is unique enough
        if len(line) == 0:
            continue
        if line not in g.console_response_log:
            similarity = check_similarity(line)
            if similarity is False and type(g.payload) is bytearray:
                g.console_response_log[line] = g.payload
                pv.normal_print("Found new console response (%d found)" % len(g.console_response_log.keys()))