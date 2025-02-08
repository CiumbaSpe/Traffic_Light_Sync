import math
import datetime

CONFIDENCE = 0.95
ALPHA = 1 - CONFIDENCE
TLS_TOTAL_TIME = 60
CONFIGURATION = (TLS_TOTAL_TIME)//2
# CONFIGURATION = 4
TANGENTIAL_FLOW = 0.6
ROU_PATH = "lightSync.rou.xml"
CONFIGURATION_STEP = 1
RUNS = 10
STEP = 50000
WARM_UP = 10000
NAME = f"results/results_t30/06/{datetime.datetime.now().strftime('%Y%m%d_%H%M')}"
SEMAPHORES = 4
