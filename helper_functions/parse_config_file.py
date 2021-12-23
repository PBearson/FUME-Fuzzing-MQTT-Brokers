import globals as g

# Parse the supplied config file
def parse_config_file(config):
    for line in config:

        # Only valid key-value pairs
        line = line.strip()
        line = line.replace(" ","")

        # The user can use @@ to re-insert spaces if they need to - for 
        # example, if the start command requires multiple words (e.g.,
        # "node <script location>")
        line = line.replace("@@", " ")
        if len(line) == 0 or line[0] == '#':
            continue
    
        # Split into key-value pairs
        arg = line.split("=")
        if len(arg) != 2:
            continue

        if arg[0] == 'CHOOSE_MUTATION':
            g.CHOOSE_MUTATION = float(arg[1])

        elif arg[0] == 'PACKET_SELECTION_UNIFORM_DISTRIBUTION':
            g.PACKET_SELECTION_UNIFORM_DISTRIBUTION = int(arg[1])

        elif arg[0] == 'FUZZING_STATE_UNIFORM_DISTRIBUTION':
            g.FUZZING_STATE_UNIFORM_DISTRIBUTION = int(arg[1])

        elif arg[0] == 'FUZZING_INTENSITY':
            g.FUZZING_INTENSITY = float(arg[1])

        elif arg[0] == 'CONSTRUCTION_INTENSITY':
            g.CONSTRUCTION_INTENSITY = int(arg[1])

        elif arg[0] == 'X1':
            g.X1 = float(arg[1])
            g.user_supplied_X[0] = 1

        elif arg[0] == 'X2':
            g.X2 = float(arg[1])
            g.user_supplied_X[1] = 1

        elif arg[0] == 'X3':
            g.X3 = float(arg[1])
            g.user_supplied_X[2] = 1

        elif arg[0] == 'b':
            g.b = float(arg[1])

        elif arg[0][0] == 'c':
            # Assertion to make sure we give a proper ci key
            assert arg[0][1:] in [str(i) for i in range(1, 16)]
            index = int(arg[0][1:]) - 1
            g.c[index] = float(arg[1])

        elif arg[0][0] == 'd':
            # Assertion to make sure we give a proper di key
            assert arg[0][1:] in [str(i) for i in range(1, 5)]
            index = int(arg[0][1:]) - 1
            g.d[index] = float(arg[1])

        elif arg[0] == 'TARGET_ADDR':
            g.TARGET_ADDR = arg[1]

        elif arg[0] == 'TARGET_PORT':
            g.TARGET_PORT = int(arg[1])

        elif arg[0] == 'VERBOSITY':
            g.VERBOSITY = int(arg[1])

        elif arg[0] == 'START_COMMAND':
            g.START_COMMAND = arg[1]

        elif arg[0] == "TARGET_START_TIME":
            g.TARGET_START_TIME = float(arg[1])

        elif arg[0] == 'SIMILARITY_THRESHOLD':
            g.SIMILARITY_THRESHOLD = float(arg[1])

        elif arg[0] == 'TRIAGE_FAST':
            g.TRIAGE_FAST = int(arg[1])

        elif arg[0] == 'TRIAGE_MAX_DEPTH':
            g.TRIAGE_MAX_DEPTH = int(arg[1])

        elif arg[0] == 'CRASH_DIRECTORY':
            g.CRASH_DIRECTORY = arg[1]

        elif arg[0] == 'CRASH_FILENAME_PREFIX':
            g.CRASH_FILENAME_PREFIX = arg[1]



        else:
            print("Unrecognized key in config file: %s" % arg[0])
            exit(-1)