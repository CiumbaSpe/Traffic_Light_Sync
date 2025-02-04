
from simulator import Simulation
from utils import plot_simulation_graph
from setting import * 
from stats import Statistics

def main():

    print(f"Numner of permutations over {SEMAPHORES} semaphores: {PERMUTATIONS}")
    print(f"Number of configurations: {CONFIGURATION} different offsets")
    print(f"Number of runs per configuration: {RUNS}")
    print(f"Numebr of steps per runs: {STEP}")
    print(f"Number of warm-up steps: {WARM_UP}")
    print(f"Results will be saved in {NAME}\n")

    sim = Simulation()
    stats = Statistics()    

    config = sim.multiple_runs()

    stats.save_stats(stats.evaluate_metrics(config, sim), index=True)

    # Plot the simulation graph
    # plot_simulation_graph(sim_step, 1000, completed_lifetimes)

if __name__ == "__main__":
    main()
