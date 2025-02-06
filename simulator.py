import traci
import os
import setting
from tracker import PerformanceTracker

class Simulation: 
    def __init__(self):
        self.warm_up = setting.WARM_UP                          # warm-up period
        self.runs = setting.RUNS                                # number of runs
        self.configuration = setting.CONFIGURATION              # number of configurations
        self.configuration_step = setting.CONFIGURATION_STEP    # how much configuration iterates
        self.track = PerformanceTracker()

    def simulation_run(self, configuration=0, gui=False):
        """ single simulation run """
        sumoBinary = 'sumo-gui' if gui else 'sumo'
        sumoBinary = os.popen(f'which {sumoBinary}').read().strip()

        sumoCmd = [sumoBinary, "-c", "lightSync.sumocfg", "--random"]
        traci.start(sumoCmd)

        track = PerformanceTracker() # create the object in which to store performance metrics of the run

        step = 0 
        # Get a list of all traffic light IDs 
        traffic_light_ids = traci.trafficlight.getIDList()
        
        # Set the offset for each traffic light
        for tl_id in traffic_light_ids: 
            traci.trafficlight.setPhase(tl_id, 0)
            for _ in range(configuration):
                step += 1
                traci.simulationStep()

        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()
            if(step > self.warm_up):
                track.update()
            step += 1

        track.simulation_end()
        traci.close(False) # close the connection to SUMO

        return track

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
            completed_lifetimes = self.simulation_run(configuration, gui=False)
            observations.append(completed_lifetimes)
        return observations

if __name__ == '__main__':
    pass













