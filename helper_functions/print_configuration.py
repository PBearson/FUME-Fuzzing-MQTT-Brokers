import globals as g

# Print configuration parameters
def print_configuration():
    if g.VERBOSITY == 0:
        return

    print("----------------------------------------------")
    print("-------- Fuzzing Engine Configuration --------")
    print("TARGET_ADDR: %s" % g.TARGET_ADDR)
    print("TARGET_PORT: %s" % g.TARGET_PORT)
    print("X1: %s" % g.X1)
    print("X2: %s" % g.X2)
    print("X3: %s" % g.X3)

    if g.VERBOSITY == 1:
        return
    print("CHOOSE_MUTATION: %s" % g.CHOOSE_MUTATION)
    print("PACKET_SELECTION_UNIFORM_DISTRIBUTION: %s" % g.PACKET_SELECTION_UNIFORM_DISTRIBUTION)
    print("FUZZING_STATE_UNIFORM_DISTRIBUTION: %s" % g.FUZZING_STATE_UNIFORM_DISTRIBUTION)
    print("FUZZING INTENSITY: %s" % g.FUZZING_INTENSITY)
    print("CONSTRUCTION_INTENSITY: %s" % g.CONSTRUCTION_INTENSITY)
    print("b: %s" % g.b)
    print("c1: %s" % g.c[0])
    print("c2: %s" % g.c[1])
    print("c3: %s" % g.c[2])
    print("c4: %s" % g.c[3])
    print("c5: %s" % g.c[4])
    print("c6: %s" % g.c[5])
    print("c7: %s" % g.c[6])
    print("c8: %s" % g.c[7])
    print("c9: %s" % g.c[8])
    print("c10: %s" % g.c[9])
    print("c11: %s" % g.c[10])
    print("c12: %s" % g.c[11])
    print("c13: %s" % g.c[12])
    print("c14: %s" % g.c[13])
    print("c15: %s" % g.c[14])
    print("d1: %s" % g.d[0])
    print("d2: %s" % g.d[1])
    print("d3: %s" % g.d[2])
    print("d4: %s" % g.d[3])
    print("----------------------------------------------")