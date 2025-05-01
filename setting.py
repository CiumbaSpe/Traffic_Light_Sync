###  Simulation parameters
TLS_TOTAL_TIME = 30                         # total step time of the TLS
# CONFIGURATION = (TLS_TOTAL_TIME)//2 + 1     # number of configurations (offsets)
CONFIGURATION = 2
TANGENTIAL_FLOW = [0.3]           # list of lambda value for exponential distribution
CONFIGURATION_STEP = 1                      # offset on the offset, 1 to try all 
RUNS = 2                                   # number of runs per configuration
STEP = 300                                # number of steps per run
WARM_UP = 2                              # number of warm-up steps
NAME = "test"                               # name of the output file      

### Other costants
CONFIDENCE = 0.95
ALPHA = 1 - CONFIDENCE
SEMAPHORES = 4
ROU_PATH = "lightSync.rou.xml"              

# FLUSSES = [0.3, 0.325, 0.35, 0.375, 0.4, 0.425, 0.45, 0.475, 0.5] 
