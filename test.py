from simulator import Simulation
from stats import Statistics

def test_simulator():
    sim = Simulation(junction=["J1"])
    sim.simulation_run(configuration=15, gui=True)

    # sim.runs = 3
    # sim.configuration_step = 1
    # conf = []
    # conf.append(sim.specific_config(configuration=0))
    # # conf.append(sim.specific_config(configuration=7))
    # conf.append(sim.specific_config(configuration=14))

    # # conf.append(sim.specific_config(configuration=15))
    # sim.configuration = len(conf)

    # # obs.append(sim.specific_config(configuration=20))

    # stats = Statistics()
    # stats.name = "results/prova/01/"
    # stats.evaluate_metrics(conf, sim)
    # # stats.save_stats(df, index=True)

if __name__ == '__main__':
    test_simulator()
    
