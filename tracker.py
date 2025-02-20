import traci
import traci._junction
import itertools

NETWORK_JUNCTION = ["J1", "J2", "J3", "J4"]
DIRECTIONS = ["tang", "tras"]

class PerformanceTracker:
    """
        Manages the update of trackers placed at junctions.
    """
    def __init__(self):
        
        self.metrics_for_stats: dict[str, float | int | list[float]] = {
            'stop_time': 0,
            'completed_lifetimes': [],
        }
        self.T = 0

        self.subtracker = [JointTracker(DIRECTIONS[0]), JointTracker(DIRECTIONS[1])]
        self.name = "Network"

    def update(self):
        self.T += 1
        for vehicle_id in traci.vehicle.getIDList():
            for subtracker in self.subtracker:
                subtracker.T = self.T
                subtracker.incoming_vehicles(vehicle_id)
                subtracker.outgoing_vehicles(vehicle_id)

        for subtracker in self.subtracker:
            if subtracker.request_monitor:
                subtracker.request_monitor = False
                subtracker.rq_time += 1

    def simulation_end(self):
        for subtracker in self.subtracker:
            subtracker.simulation_end()
        self.metrics_for_stats['stop_time'] = sum([subtracker.metrics_for_stats['stop_time'] for subtracker in self.subtracker])
        self.metrics_for_stats['completed_lifetimes'] = list(itertools.chain.from_iterable([subtracker.metrics_for_stats['completed_lifetimes'] for subtracker in self.subtracker]))
        

class JointTracker():
    def __init__(self, direction: str):

        self.vehicle_lifetimes = {}
        self.metrics_for_stats: dict[str, float | int | list[float]] = {
            'stop_time': 0,
            'completed_lifetimes': [],
            'arrival_rate': 0.0,
            'throughput': 0.0,
            'utilization': 0.0,
            'average_time_service': 0.0,
            'completed': 0,
        }
        self.T = 0
        self.arrivals = 0   # number of vehicles that arrived in the system
        self.completed = 0  # number of vehicles that completed their trip
        self.rq_time = 0    # time in which there is at least one request in the system

        self.incoming_routes = []
        self.outgoing_routes = []
        self.incoming_junctions = []

        for junction in NETWORK_JUNCTION:
            self.outgoing_routes.append([e for e in traci.junction.getOutgoingEdges(junction) if not e.startswith(":") and e.endswith(direction)])
            self.incoming_routes.append([e for e in traci.junction.getIncomingEdges(junction) if not e.startswith(":") and e.endswith(direction)])
            self.incoming_junctions.append([e for e in traci.junction.getIncomingEdges(junction) if e.startswith(":") and e.endswith(direction)])

        self.outgoing_routes = list(itertools.chain.from_iterable(self.outgoing_routes))
        self.incoming_routes = list(itertools.chain.from_iterable(self.incoming_routes))

        self.name = f"Network_{direction}"
        self.request_monitor = False


    def incoming_vehicles(self, vehicle_id):
        current_edge = traci.vehicle.getRoadID(vehicle_id)
        vehicle_speed = traci.vehicle.getSpeed(vehicle_id)

        # Check if vehicle is on junctions or (on incoming routes and stopped)
        is_relevant_edge = (current_edge in self.incoming_junctions or 
                  (current_edge in self.incoming_routes and vehicle_speed < 0.1))
        
        # Process new vehicles
        if is_relevant_edge and vehicle_id not in self.vehicle_lifetimes:
            self.request_monitor = True
            self.arrivals += 1
            self.vehicle_lifetimes[vehicle_id] = traci.simulation.getTime()

        # Track stopped vehicles
        if vehicle_speed < 0.1:
            self.metrics_for_stats['stop_time'] += 1



    def outgoing_vehicles(self, vehicle_id):
        current_edge = traci.vehicle.getRoadID(vehicle_id)
        if current_edge in self.outgoing_routes:
            # Calculate the lifetime and store it
            depart_time = self.vehicle_lifetimes.pop(vehicle_id, None)
            if depart_time is not None:
                self.completed += 1
                lifetime = traci.simulation.getTime() - depart_time
                self.metrics_for_stats['completed_lifetimes'].append(lifetime)
       
    def simulation_end(self):
        self.metrics_for_stats['arrival_rate'] = self.arrivals / self.T
        self.metrics_for_stats['throughput'] = self.completed / self.T
        self.metrics_for_stats['utilization'] = self.rq_time / self.T
        self.metrics_for_stats['average_time_service'] = self.rq_time / self.completed
        self.metrics_for_stats['completed'] = self.completed
        # self.metrics_for_stats['visit_count'] = self.completed/Network_completed
        # self.metrics_for_stats['service_demand'] = self.metrics_for_stats['visit_count'] * self.metrics_for_stats['average_time_service']

        
if __name__ == "__main__":
    track = PerformanceTracker()
    # Cycle through all keys and values in self.metrics_for_stats
    for key, value in track.metrics_for_stats.items():
        print(key)
        