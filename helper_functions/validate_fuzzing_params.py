import globals as g

# CONSTRUCTION_INTENSITY must be a non-negative integer
def validate_construction_intensity():
    assert int(g.CONSTRUCTION_INTENSITY) == g.CONSTRUCTION_INTENSITY
    assert g.CONSTRUCTION_INTENSITY >= 0

# FUZZING_INTENSITY must be in the range [0...1]
def validate_fuzzing_intensity():
    assert g.FUZZING_INTENSITY >= 0 and g.FUZZING_INTENSITY <= 1

# FUZZING_STATE_UNIFORM_DISTRIBUTION must be binary
def validate_fuzzing_state_uniform_distribution():
    assert g.FUZZING_STATE_UNIFORM_DISTRIBUTION in [0, 1]

# PACKET_SELECTION_UNFIROM_DISTRIBUTION must be binary
def validate_packet_selection_uniform_distribution():
    assert g.PACKET_SELECTION_UNIFORM_DISTRIBUTION in [0, 1]

# CHOOSE_MUTATION must be in the range [0...1]
def validate_choose_mutation():
    assert g.CHOOSE_MUTATION <= 1 and g.CHOOSE_MUTATION >= 0

# X1, X2, and X3 must be in the range [0...1]
def validate_X():
    assert g.X1 <= 1 and g.X1 >= 0
    assert g.X2 <= 1 and g.X2 >= 0
    assert g.X3 <= 1 and g.X3 >= 0

# b must be in the range [0...1]
def validate_b():
    assert g.b <= 1 and g.b >= 0

# The values in c must sum to 1
def validate_c():
    sum = 0
    for ci in g.c:
        sum += ci
    assert abs(sum - 1) < 0.00001 

# The first 3 values in c must sum to 1
# The last value in d must be in the range [0...1]
def validate_d():
    sum = 0
    for di in g.d[0:3]:
        sum += di
    assert abs(sum - 1) < 0.00001 
    assert g.d[3] <= 1 and g.d[3] >= 0

# Validate all parameters of the fuzzing engine
def validate_all():
    validate_X()
    validate_b()
    validate_c()
    validate_d()
    validate_choose_mutation()
    validate_packet_selection_uniform_distribution()
    validate_fuzzing_state_uniform_distribution()
    validate_fuzzing_intensity()
    validate_construction_intensity()