import traci
import os
from tracker import PerformanceTracker, JointTracker
from tls import TrafficLightSystem

class Simulation: 
    def __init__(self, simulation_steps: int, warm_up: int, number_of_runs: int):
        self.warm_up = warm_up                                  # warm-up period
        self.runs = number_of_runs                              # number of runs
        self.simulation_steps = simulation_steps                # simulation steps        

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

    def specific_config(self, configuration):
        """ Run the simulation with a specific configuration for self.runs times """
        observations = []
        for i in range(self.runs):
            print(f"### Running simulation {i}")
            observations.append(self.simulation_run(configuration, gui=False))
        return observations

if __name__ == '__main__':
    pass













