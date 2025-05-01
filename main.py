from simulator import Simulation
from utils import display_setting, modify_rou_flow_rate
from stats import Statistics
import setting

def main():

    # Display the simulation settings
    display_setting()

    # Create an instance of the Simulation class (it will handle the simulation logic)
    # And the Statistics class  (at the end of the simulation it will handle statistics with the recorded data)
    sim = Simulation()
    stats = Statistics()    

    # For each flow rate in the list, modify the XML file and run the simulation
    for i in setting.TANGENTIAL_FLOW:
        modify_rou_flow_rate(setting.ROU_PATH, i)
    
        config = sim.multiple_runs()
        sim.configuration = len(config)

        stats.evaluate_metrics(config, sim)


    # TODO: refactor this
    # Plot the simulation graph
    # plot_simulation_graph(sim_step, 1000, completed_lifetimes)

if __name__ == "__main__":
    main()
