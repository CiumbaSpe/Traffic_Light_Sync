from simulator import Simulation
from stats import Statistics
from utils import plot_simulation_graph, modify_rou_flow_rate
import setting

def test_throughput():
    """
    Test the throughput of the simulation.
    """
    sim = Simulation(setting.STEP, setting.WARM_UP, 20)
    stats = Statistics()

    conf = []
    for i in [0.5, 0.525, 0.55, 0.575, 0.6, 0.625, 0.65, 0.675, 0.7]:
        print(f"### Running simulation with flow rate {i}")
        modify_rou_flow_rate('lightSync.rou.xml', i, setting.STEP)
        conf.append(sim.specific_config(configuration=15))
    
    stats.name = f"results/prova/TightFluss/"
    stats.evaluate_metrics(conf)


def test_simulator():
    
    modify_rou_flow_rate('lightSync.rou.xml', 0.3, setting.STEP)  # Change 'input.xml' to the path of your XML file
    sim = Simulation(setting.STEP, setting.WARM_UP, 1)

    conf = []
    # conf.append(sim.specific_config(configuration=0))
    # conf.append(sim.specific_config(configuration=7))
    conf.append(sim.specific_config(configuration=15))
    # conf.append(sim.specific_config(configuration=15))


    stats = Statistics()
    stats.name = "results/prova/subscription1/"

    stats.evaluate_metrics(conf)

    plot_simulation_graph(conf[0][0][1].metrics_for_stats['completed_lifetimes'], conf[0][0][1].completed_at_time)

if __name__ == '__main__':
    test_throughput()
    # test_simulator()
    
