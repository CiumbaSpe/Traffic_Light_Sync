from simulator import Simulation
from stats import Statistics
from tls import TrafficLightSystem

def test_simulator():
    sim = Simulation()

    sim.runs = 3
    sim.configuration = 3
    sim.configuration_step = 1
    obs = []
    obs.append(sim.specific_config(configuration=0))
    obs.append(sim.specific_config(configuration=5))
    obs.append(sim.specific_config(configuration=14))

    stats = Statistics()
    df = stats.evaluate_metrics(obs, sim)
    stats.save_stats(df, index=True)

if __name__ == '__main__':
    test_simulator()
    
