# TODO write a crash triage function that loads the request queue dump file, finds the input that causes the crash, then gradually tries to reduce the size of the input until it is minimized

# We can have a set of candidate inputs. We add an input to that set
# when it is smaller than the current best input. After we perform all
# of our operations, we select the smallest input from the candidate set. Then we repeat until we have an input that does not get any smaller.

import socket
import sys
import time
import subprocess
import random
from fume.run_target import check_connection 
import globals as g
import helper_functions.print_verbosity as pv
import helper_functions.parse_config_file as pcf
import fume.run_target as rt

buffer = []
buffer_len = 10

# Sometimes the broker will crash a moment or 2 after a bad packet is sent.
# If a new (non-buggy) packet has already been sent by then, we may falsely
# believe the new packet is responsible for the crash. Therefore, we use a 
# buffer to hold the most recent packets and call this function to verify
# the responsible packet.
def check_buffer():
    global buffer

    for b in reversed(buffer):
        status = check_input(b, 0.25)
        if status == False:
            return b

    # Either false positive, or the buffer did not capture the correct packet :(
    pv.normal_print("A crash was detected, but it could not be replicated.")
    return None 

# Check the crash log for the payload which is responsible for the crash.
def check_crash_log(crash_log):
    for c in reversed(crash_log):
        c_bytes = bytearray.fromhex(c)
        status = check_input(c_bytes, 0.25)
        if status == False:
            pv.normal_print("A crash was detected from the following input: %s" % c)
            return c_bytes
    pv.print_error("The crash log does not seem to contain a payload which crashes this target.")
    exit(-1)

def update_buffer(input):
    global buffer
    buffer.append(input)
    if len(buffer) > buffer_len:
        buffer.pop(0)

def start_target():
    process = subprocess.Popen(g.START_COMMAND.split(), stdout = subprocess.DEVNULL, stderr = subprocess.STDOUT)

    # Try to connect to the target
    pv.verbose_print("Starting target...")
    for i in range(10):
        pv.debug_print("Attempt %d" % (i + 1))
        time.sleep(g.TARGET_START_TIME * ((i + 1)/5))
        alive = rt.check_connection()
        if alive:
            pv.verbose_print("Target started successfully!")
            return

    pv.print_error("Could not start target")
    exit(-1)

# Check if the input causes a crash. If it does, return True.
# Else return False
def check_input(input, sleep_time = 0.01):
    # TODO there may be times were the close() function fails because the send() function crashes the broker. We need to consider this.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            s.connect((g.TARGET_ADDR, g.TARGET_PORT))
            s.send(input)      
            s.close()
            break
        except ConnectionResetError:
            continue
        except ConnectionRefusedError:
            break

    time.sleep(sleep_time)
    return rt.check_connection()
    
# Return an input with a block of size mutate_size changed to 
# 'A' bytes, beginning at the index.
def mutate_block(input, index, mutate_size):
    # TODO
    return input


# Delete from random indices in the input
def delete_random(input, delete_size):
    for d in range(delete_size):
        index = random.randint(0, len(input) - 1)
        input = input[:index] + input[index + 1:]
    return input

# Return an input with a block of size delete_size removed,
# beginning at the index.
def delete_block(input, index, delete_size):
    return input[:index] + input[index + delete_size:]

def check_for_crash(input, candidates, local_candidates):
    crash_status = check_input(input)
    update_buffer(input)

    # False crash status means the target actually crashed
    if crash_status is False:

        # Restart the target
        start_target()

        # Check which input actually caused the crash
        new_input = check_buffer()
        
        # If None, then the target did not crash
        if new_input is None:
            return

        # Restart the target since check_buffer() crashed it
        start_target()

        # Log the input if it is unique
        if new_input not in candidates:

            # In the fast version, we only log a single candidate, and 
            # we only update that candidate when we find a smaller one
            if g.TRIAGE_FAST:
                if len(candidates) == 0:
                    candidates.append(new_input)
                    pv.normal_print("Found new crash: %s" % new_input.hex())
                elif len(new_input) < len(candidates[0]):
                    candidates[0] = new_input
                    pv.normal_print("Found new crash: %s" % new_input.hex())
                
            # In the slow version, we log all new candidates that we find
            else:
                candidates.append(new_input)
                local_candidates.append(new_input)
                pv.normal_print("Found new crash: %s" % new_input.hex())

    return candidates, local_candidates


# Triage the current input and return a tuple of (reduced_input, new_candidates)
# where reduced_input is a smaller input that still crashes the target,
# and new_candidates is any intermediate inputs we found on the way
def triage(input, candidates = [], triage_level = 1):
    if triage_level > g.TRIAGE_MAX_DEPTH:
        return input, []

    pv.normal_print("Triaging input %s" % input.hex())
    start_size = len(input)
    delete_size = 1
    local_candidates = []

    # Delete bytes for as long as possible
    while delete_size < len(input):
        pv.verbose_print("Delete size is now %d" % delete_size)
        i = 0

        # Delete a block of size delete_size at index i
        while i + delete_size <= len(input):
            new_input = delete_block(input, i, delete_size)
            check_for_crash(new_input, candidates, local_candidates)
            i += 1

        # Delete delete_size number of bytes at random indices
        random_iterations = round(len(input) / delete_size)
        for j in range(random_iterations):
            new_input = delete_random(input, delete_size)
            check_for_crash(new_input, candidates, local_candidates)

        # Update the delete size
        delete_size *= 2

    # For each new candidate found in this instance, recursively triage them.
    # As newer, smaller candidates are found, update the input

    # In the fast version, we only worry about the single candidate we logged
    if g.TRIAGE_FAST:
        if len(candidates) > 0:
            new_candidate, _ = triage(candidates[0], [], triage_level + 1)
            if len(new_candidate) < len(input):
                input = new_candidate

    # In the slow version, we iterate over all new candidates we found
    else:
        for candidate in local_candidates:
            new_candidate, new_locals = triage(candidate, candidates, triage_level + 1)
            if len(new_candidate) < len(input):
                input = new_candidate
            for local in new_locals:
                if local not in candidates:
                    candidates.append(local)

    # Calculate the percent decrease in the input size
    end_size = len(input)
    if end_size < start_size:
        reduction = 100 * (1 - (float(end_size) / float(start_size)))
        pv.normal_print("Input size reduced by %f%% (we are %d triage levels deep)" % (reduction, triage_level))
    else:
        pv.normal_print("Input size did not change (we are %d triage levels deep)" % triage_level)

    # Return the new input
    return input, local_candidates
    
if __name__ == "__main__":
    # Try to parse the supplied config file.
    try:
        config_f = open(sys.argv[2], 'r')
        config = config_f.readlines()
        pcf.parse_config_file(config)
        config_f.close()
    except FileNotFoundError:
        pv.print_error("Could not find the supplied config file file: %s" % sys.argv[2])
        exit(-1)
    except IndexError:
        pv.print_error("Usage: triage.py <crash log file> <config file>")
        exit(-1)

    # Load the crash log
    try:
        crash_f = open(sys.argv[1], 'r')
        crash_log = crash_f.readlines()
        config_f.close()
    except FileNotFoundError:
        pv.print_error("Could not find the supplied crash file: %s" % sys.argv[1])
        exit(-1)
    except IndexError:
        pv.print_error("Usage: triage.py <crash log file> <config file>")
        exit(-1)

    # Start the target
    start_target()

    # Find the right input from the crash log
    input = check_crash_log(crash_log)

    # Restart the target, since check_crash_log() probably crashed it
    start_target()

    # Triage the input
    if g.TRIAGE_FAST:
        pv.normal_print("Using the FAST version")
    else:
        pv.normal_print("Using the SLOW version")

    run = 1
    first_start_size = len(input)
    while True:
        pv.normal_print("RUN #%d" % run)
        start_size = len(input)
        input, _ = triage(input)
        end_size = len(input)
        reduction = 100 * (1 - (float(end_size) / float(start_size)))
        if end_size == start_size:
            print("Input size did not change.")
            break
        else:
            print("New input: %s\nReduced by %f%%" % (input.hex(), reduction))
            run += 1

    reduction = 100 * (1 - (float(end_size) / float(first_start_size)))
    print("FINAL INPUT: %s\nReduced by %f%%" % (input.hex(), reduction))