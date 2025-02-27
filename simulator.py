import traci
import os
import setting
from tracker import PerformanceTracker, JointTracker
from tls import TrafficLightSystem
from utils import modify_rou_flow_rate

class Simulation: 
    def __init__(self):
        self.warm_up : int = setting.WARM_UP                          # warm-up period
        self.runs : int = setting.RUNS                                # number of runs
        self.configuration : int = setting.CONFIGURATION              # number of configurations
        self.configuration_step : int = setting.CONFIGURATION_STEP    # how much configuration iterates
        self.simulation_steps : int = setting.STEP                    # simulation steps        

    def simulation_run(self, configuration: int = 0, gui=False):
        """ single simulation run """
        sumoBinary = 'sumo-gui' if gui else 'sumo'
        sumoBinary = os.popen(f'which {sumoBinary}').read().strip()

        sumoCmd = [sumoBinary, "-c", "lightSync.sumocfg", "--random"]
        traci.start(sumoCmd)
        
        net_tracker = PerformanceTracker()

        TrafficLightSystem(traci.trafficlight.getIDList(), config=configuration)

        step = traci.simulation.getTime()

        while traci.simulation.getMinExpectedNumber() > 0 and step < self.simulation_steps:
            traci.simulationStep()
            if(step > self.warm_up):
                net_tracker.update()
            step += 1

        net_tracker.simulation_end()
        traci.close(False) # close the connection to SUMO

        trackers = [net_tracker]
        for subtracker in net_tracker.subtracker:
            trackers.append(subtracker)

        return trackers

    def multiple_fluss(self, fluss : list[float]):
        """ Run the simulation with multiple flow rates """
        config = [] # it will store m flows configuration
        for f in fluss:
            print(f"====== Running fluss {f} ======")
            modify_rou_flow_rate(setting.ROU_PATH, f)
            config.append(self.specific_config(15))
        return config


    def multiple_runs(self): # systematically try all combinations of parameters
        """ Run the simulation with all possible combinations of parameters """
        config = [] # it will store m configurations
        for offset in range(0, self.configuration, self.configuration_step):
            print(f"====== Running configuration {offset//self.configuration_step} ======")
            config.append(self.specific_config(offset))
        return config

    def specific_config(self, configuration):
        """ Run the simulation with a specific configuration for self.runs times """
        observations = []
        for i in range(self.runs):
            print(f"### Running simulation {i}")
            observations.append(self.simulation_run(configuration, gui=False))
        return observations

if __name__ == '__main__':
    pass













