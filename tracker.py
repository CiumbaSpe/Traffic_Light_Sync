import traci
import traci._junction

class PerformanceTracker:
    """
    Tracks various performance metrics of the simulation.
    """
    def __init__(self, subtracker: list['JointTracker'] | None = None):
        self.vehicle_lifetimes = {}
        self.name = "Network"
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
        self.subtracker = subtracker

    def update(self):
        self.T += 1
        there_is_request = False
        for vehicle_id in traci.vehicle.getIDList():
            there_is_request = True
            self.incoming_vehicles(vehicle_id)
            if(self.subtracker is not None):
                for subtracker in self.subtracker:
                    subtracker.T = self.T
                    subtracker.incoming_vehicles(vehicle_id)
                    if subtracker.request_monitor:
                        subtracker.request_monitor = False
                        subtracker.rq_time += 1
                    subtracker.outgoing_vehicles(vehicle_id)
        
        self.outgoing_vehicles()

        if(there_is_request):
            self.rq_time += 1

    def incoming_vehicles(self, vehicle_id):
        # Get a list of all vehicles currently in the simulation
        if vehicle_id not in self.vehicle_lifetimes:    # If the vehicle is seen for the first time, record its departure time
            self.arrivals += 1
            self.vehicle_lifetimes[vehicle_id] = traci.vehicle.getDeparture(vehicle_id)
        
        if traci.vehicle.getSpeed(vehicle_id) < 0.1:    # If the vehicle's speed is close to 0, increment stop_time
            self.metrics_for_stats['stop_time'] += 1
        

    def outgoing_vehicles(self):
        # Check for vehicles that completed their trips
        arrived_vehicles = traci.simulation.getArrivedIDList()
        for vehicle_id in arrived_vehicles:
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
        if(self.subtracker is not None):
            for subtracker in self.subtracker:
                subtracker.simulation_end()

class JointTracker(PerformanceTracker):
    def __init__(self, junction: str):
        super().__init__()
        self.junction = junction
        self.name = f"Junction_{junction}"
        self.request_monitor = False

        self.outgoing_routes = [e for e in traci.junction.getOutgoingEdges(junction) if not e.startswith(":")]
        self.incoming_routes = [e for e in traci.junction.getIncomingEdges(junction) if not e.startswith(":")]

    def incoming_vehicles(self, vehicle_id):
        current_edge = traci.vehicle.getRoadID(vehicle_id)
        if current_edge in self.incoming_routes: 
            self.request_monitor = True
            if vehicle_id not in self.vehicle_lifetimes:
                self.arrivals += 1
                self.vehicle_lifetimes[vehicle_id] = traci.simulation.getTime()
            
            if traci.vehicle.getSpeed(vehicle_id) < 0.1:
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
       

if __name__ == "__main__":
    track = PerformanceTracker()
    # Cycle through all keys and values in self.metrics_for_stats
    for key, value in track.metrics_for_stats.items():
        print(key)
        