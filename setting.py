import time

###  Simulation parameters
TLS_TOTAL_TIME = 30                             # total step time of the TLS
CONFIGURATION = (TLS_TOTAL_TIME)//2 + 1         # number of configurations (offsets)
# CONFIGURATION = 2
TANGENTIAL_FLOW = [0.3, 0.4, 0.5]               # list of lambda value for exponential distribution
CONFIGURATION_STEP = 1                          # offset on the offset, 1 to try all 
RUNS = 20                                       # number of runs per configuration
STEP = 50_000                                   # number of steps per run
WARM_UP = 6000                                  # number of warm-up steps

### Other costants
CONFIDENCE = 0.95
ALPHA = 1 - CONFIDENCE
SEMAPHORES = 4
ROU_PATH = "lightSync.rou.xml"              
NAME = f"{time.strftime('%Y%m%d_%H%M%S')}"  # name of the directory inside /results (auto created) where stats will be saved

