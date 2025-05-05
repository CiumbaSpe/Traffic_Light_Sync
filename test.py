from simulator import Simulation
from stats import Statistics
from utils import plot_simulation_graph
import setting

def test_simulator():
    sim = Simulation(setting.STEP, setting.WARM_UP, 2)
    # sim.simulation_run(configuration=15, gui=True)

    conf = []
    # conf.append(sim.specific_config(configuration=0))
    # conf.append(sim.specific_config(configuration=7))
    conf.append(sim.specific_config(configuration=15))

    # conf.append(sim.specific_config(configuration=15))
    sim.configuration = len(conf)

    # obs.append(sim.specific_config(configuration=20))

    stats = Statistics()
    stats.name = "results/prova/subscription1/"
    stats.evaluate_metrics(conf)

    # plot_simulation_graph(setting.STEP, setting.WARM_UP, conf[0][0][0].metrics_for_stats['completed_lifetimes'])
    # plot_simulation_graph(setting.STEP, setting.WARM_UP, conf[0][0][1].metrics_for_stats['completed_lifetimes'])
    # plot_simulation_graph(setting.STEP, setting.WARM_UP, conf[0][1][1].metrics_for_stats['completed_lifetimes'], name="image_1.png")
    # plot_simulation_graph(setting.STEP, setting.WARM_UP, conf[0][0][2].metrics_for_stats['completed_lifetimes'], name="image_2.png")
    # plot_simulation_graph(setting.STEP, setting.WARM_UP, conf[0][1][2].metrics_for_stats['completed_lifetimes'], name="image_3.png")

if __name__ == '__main__':
    test_simulator()
    
