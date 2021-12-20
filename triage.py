# TODO write a crash triage function that loads the request queue dump file, finds the input that causes the crash, then gradually tries to reduce the size of the input until it is minimized

# We can have a set of candidate inputs. We add an input to that set
# when it is smaller than the current best input. After we perform all
# of our operations, we select the smallest input from the candidate set. Then we repeat until we have an input that does not get any smaller.

import socket
import sys
import time
import subprocess
from fume.run_target import check_connection 
import globals as g
import helper_functions.print_verbosity as pv
import helper_functions.parse_config_file as pcf
import fume.run_target as rt

def start_target():
    process = subprocess.Popen([g.START_COMMAND], stdout = subprocess.DEVNULL, stderr = subprocess.STDOUT)

    # Try to connect to the target
    pv.verbose_print("Starting target...")
    for i in range(10):
        pv.debug_print("Attempt %d" % (i + 1))
        time.sleep(g.TARGET_START_TIME * ((i + 1)/5))
        alive = rt.check_connection()
        if alive:
            pv.verbose_print("Target started successfully!")
            time.sleep(0.25)
            return

# Check if the input causes a crash. If it does, return True.
# Else return False
def check_input(input):

    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((g.TARGET_ADDR, g.TARGET_PORT))
            s.send(input)
            s.close()
            break
        except (ConnectionResetError, ConnectionRefusedError):
            pv.normal_print("Connection error. Trying again...")
            time.sleep(0.1)
            continue

    time.sleep(0.25)

    connection_status = rt.check_connection()
    
    return connection_status

# Return an input with a block of size mutate_size changed to 
# 'A' bytes, beginning at the index.
def mutate_block(input, index, mutate_size):
    # TODO
    return input


# Delete from random indices in the input
def delete_random(input, delete_size):
    # TODO
    return input

# Return an input with a block of size delete_size removed,
# beginning at the index.
def delete_block(input, index, delete_size):
    return input[:index] + input[index + delete_size:]

def triage(input, candidates = [], triage_level = 1):
    pv.normal_print("Triaging input %s" % input.hex())
    start_size = len(input)
    delete_size = 1
    local_candidates = []

    while delete_size < len(input):
        pv.verbose_print("Delete size is now %d" % delete_size)
        i = 0
        while i + delete_size <= len(input):
            new_input = delete_block(input, i, delete_size)
            crash_status = check_input(new_input)

            # False crash status means the target actually crashed
            if crash_status is False:
                # Log the input if it is unique
                if new_input not in candidates:

                    # In the fast version, we only log a single candidate, and 
                    # we only update that candidate when we find a smaller one
                    if g.TRIAGE_FAST:
                        if len(candidates) == 0:
                            candidates.append(new_input)
                            print("Found new crash: %s" % new_input.hex())
                        elif len(new_input) < len(candidates[0]):
                            candidates[0] = new_input
                            print("Found new crash: %s" % new_input.hex())
                        
                    # In the slow version, we log all new candidates that we find
                    else:
                        candidates.append(new_input)
                        local_candidates.append(new_input)
                        print("Found new crash: %s" % new_input.hex())

                # Restart the target
                start_target()
            i += 1

        delete_size *= 2

    # For each new candidate found in this instance, recursively triage them.
    # As newer, smaller candidates are found, update the input

    # In the fast version, we only worry about the single candidate we logged
    if g.TRIAGE_FAST:
        new_candidate = triage(candidates[0], candidates, triage_level + 1)
        if len(new_candidate) < len(input):
            input = new_candidate

    # In the slow version, we iterate over all new candidates we found
    else:
        for candidate in local_candidates:
            new_candidate = triage(candidate, candidates, triage_level + 1)
            if len(new_candidate) < len(input):
                input = new_candidate

    # Calculate the percent decrease in the input size
    end_size = len(input)
    if end_size < start_size:
        reduction = 100 * (1 - (float(end_size) / float(start_size)))
        pv.normal_print("Input size reduced by %f%% (we are %d triage levels deep)" % (reduction, triage_level))
    else:
        pv.verbose_print("Input size did not change (we are %d triage levels deep)" % triage_level)

    # Return the new input
    return input
    
if __name__ == "__main__":
    input = bytearray.fromhex("101e00044d5154540502003c0000117c792d6d7174742d636c69656e742d696423020001c0005002000120020002")

     # Try to parse the supplied config file.
    # If one is not supplied, use the default values.
    try:
        config_f = open(sys.argv[1], 'r')
        config = config_f.readlines()
        pcf.parse_config_file(config)
        config_f.close()
    except FileNotFoundError:
        print("Could not find the supplied file: %s" % sys.argv[1])
        exit(-1)
    except IndexError:
        print("Usage: triage.py <config file>")
        exit(-1)
    
    # Star the target
    start_target()

    # Triage the input
    start_size = len(input)
    input = triage(input)
    end_size = len(input)
    reduction = 100 * (1 - (float(end_size) / float(start_size)))
    print("New input: %s\nReduced by %f%%" % (input.hex(), reduction))