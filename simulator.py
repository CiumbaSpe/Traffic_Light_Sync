import traci
import os
import setting
from stats import Statistics
from tracker import PerformanceTracker
from utils import unique_permutations

class Simulation: 
    def __init__(self):
        self.warm_up = setting.WARM_UP                          # warm-up period
        self.permutations = setting.PERMUTATIONS                # number of permutations
        self.runs = setting.RUNS                                # number of runs
        self.configuration = setting.CONFIGURATION              # number of configurations
        self.configuration_step = setting.CONFIGURATION_STEP    # how much configuration iterates
        self.track = PerformanceTracker()

    def simulation_run(self, permutation=0, configuration=0, gui=False):
        """ single simulation run """
        sumoBinary = 'sumo-gui' if gui else 'sumo'
        sumoBinary = os.popen(f'which {sumoBinary}').read().strip()

        sumoCmd = [sumoBinary, "-c", "lightSync.sumocfg", "--random"]
        traci.start(sumoCmd)

        track = PerformanceTracker() # create the object in which to store performance metrics of the run

        step = 0 
        # Get a list of all traffic light IDs and generate all permutations
        traffic_light_ids = traci.trafficlight.getIDList()
        traffic_light_ids = unique_permutations(traffic_light_ids)
        current_tls_perm = traffic_light_ids[permutation]
        # Set the offset for each traffic light
        for tl_id in current_tls_perm: 
            traci.trafficlight.setPhase(tl_id, 0)
            for _ in range(configuration):
                traci.simulationStep()

        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()
            if(step > self.warm_up):
                track.update()
            step += 1

        traci.close(False) # close the connection to SUMO

        return track

    def multiple_runs(self): # systematically try all combinations of parameters
        """ Run the simulation with all possible combinations of parameters """
        config = [] # it will store m configurations
        for perm in range(self.permutations):
            print(f"====== Running permutation {perm} ======")
            for offset in range(0, self.configuration, self.configuration_step):
                print(f"====== Running configuration {offset//self.configuration_step} ======")
                config.append(self.specific_config(perm, offset))
        return config

    def specific_config(self, permutation, configuration):
        """ Run the simulation with a specific configuration for self.runs times """
        observations = []
        for i in range(self.runs):
            print(f"### Running simulation {i}")
            completed_lifetimes = self.simulation_run(permutation, configuration, gui=False)
            observations.append(completed_lifetimes)
        return observations

if __name__ == '__main__':
    sim = Simulation()

    tracker = sim.simulation_run()
    print(tracker.stop_time)
    tracker = sim.simulation_run(permutation=0, configuration=sim.configuration-1)
    print(tracker.stop_time)
    # sim.simulation_run(permutation=0, configuration=15, gui=True)

    # sim.runs = 2
    # sim.permutations = 1
    # sim.configuration = 2
    # sim.configuration_step = 1
    # obs = []
    # obs.append(sim.specific_config(configuration=18, permutation=0))
    # obs.append(sim.specific_config(configuration=19, permutation=0))

    # stats = Statistics()
    # df = stats.evaluate_metrics(obs, sim)
    # stats.save_stats(df, index=True)












