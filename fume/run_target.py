import globals as g
import subprocess
import threading
import time
import socket
import helper_functions.print_verbosity as pv

import fume.handle_console_response as fcr


# Check if the connection is a live
def check_connection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            s.connect((g.TARGET_ADDR, g.TARGET_PORT))
            s.close()
            return True
        except ConnectionRefusedError:
            return False
        except ConnectionResetError:
            continue


# Run the target, unless the start command is left blank
def run_target():
    if g.START_COMMAND == "":
        return

    process = subprocess.Popen(g.START_COMMAND, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    thread = threading.Thread(target=fcr.handle_console_response, args=(process,))

    thread.start()

    # Try to connect to the target
    pv.normal_print("Starting target...")
    for i in range(10):
        pv.verbose_print("Attempt %d" % (i + 1))
        time.sleep(g.TARGET_START_TIME * ((i + 1) / 5))
        alive = check_connection()
        if alive:
            pv.normal_print("Target started successfully!")
            return

    pv.print_error("It seems the target did not start successfully.")
    exit(-1)
