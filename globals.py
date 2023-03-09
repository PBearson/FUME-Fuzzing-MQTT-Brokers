# Markov variables
X1 = 0.5
X2 = 0.5
X3 = 1
b = 0.5
c = [1/15] * 15
d = [1/3, 1/3, 1/3, 1/8]

# Target parameters
TARGET_ADDR = "0.0.0.0"
TARGET_PORT = 1883

# Configuration variables
CHOOSE_MUTATION = 0.5
PACKET_SELECTION_UNIFORM_DISTRIBUTION = 1
FUZZING_STATE_UNIFORM_DISTRIBUTION = 1

# Intensity parameters
FUZZING_INTENSITY = 0.1
CONSTRUCTION_INTENSITY = 3

# Target run parameters
START_COMMAND = ""
TARGET_START_TIME = 0.5

# If 1, then the user supplied X1, X2, or X3 in the config file
user_supplied_X = [0, 0, 0]

# Verbosity
VERBOSITY = 1

# Payload -- a list of either Packet objects or strings 
# (depending on the model type)
payload = []

# The protocol version of the current payload
protocol_version = 0

# Response logs - each is a dictionary where the 
# key is a request and the value is the response
network_response_log = {}
console_response_log = {}

# Similarity threshold for console responses
SIMILARITY_THRESHOLD = 0.3

# Request queue parameters
request_queue = []
REQUEST_QUEUE_SIZE = 10

# Triage parameters
TRIAGE_FAST = 1
TRIAGE_MAX_DEPTH = 3

# Crash log parameters
CRASH_DIRECTORY = "crashes"
CRASH_FILENAME_PREFIX = "target"

# Self-explanatory 
MAXIMUM_PAYLOAD_LENGTH = 10000