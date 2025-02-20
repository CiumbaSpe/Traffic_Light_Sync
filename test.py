from simulator import Simulation
from stats import Statistics
from utils import plot_simulation_graph
import setting

def test_simulator():
    sim = Simulation()
    # sim.simulation_run(configuration=15, gui=True)

    sim.runs = 2
    sim.configuration_step = 1
    conf = []
    # conf.append(sim.specific_config(configuration=0))
    # conf.append(sim.specific_config(configuration=7))
    conf.append(sim.specific_config(configuration=14))

    # conf.append(sim.specific_config(configuration=15))
    sim.configuration = len(conf)

    # obs.append(sim.specific_config(configuration=20))

    # stats = Statistics()
    # stats.name = "results/prova/06/"
    # stats.evaluate_metrics(conf, sim)

    # plot_simulation_graph(setting.STEP, setting.WARM_UP, conf[0][0][0].metrics_for_stats['completed_lifetimes'])
    plot_simulation_graph(setting.STEP, setting.WARM_UP, conf[0][0][1].metrics_for_stats['completed_lifetimes'])
    plot_simulation_graph(setting.STEP, setting.WARM_UP, conf[0][1][1].metrics_for_stats['completed_lifetimes'])
    plot_simulation_graph(setting.STEP, setting.WARM_UP, conf[0][0][2].metrics_for_stats['completed_lifetimes'])
    plot_simulation_graph(setting.STEP, setting.WARM_UP, conf[0][1][2].metrics_for_stats['completed_lifetimes'])
if __name__ == '__main__':
    test_simulator()
    
