from simulator import Simulation
from utils import setting_to_stdout, modify_rou_flow_rate
from stats import Statistics
import setting

def main():

    setting_to_stdout()
    modify_rou_flow_rate(setting.ROU_PATH, setting.TANGENTIAL_FLOW)

    sim = Simulation()
    stats = Statistics()    

    config = sim.multiple_runs()

    
    stats.save_stats(stats.evaluate_metrics(config, sim), index=True)

    # Plot the simulation graph
    # plot_simulation_graph(sim_step, 1000, completed_lifetimes)

if __name__ == "__main__":
    main()
