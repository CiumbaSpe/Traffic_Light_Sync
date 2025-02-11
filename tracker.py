import traci
import traci._junction

class PerformanceTracker:
    """
    Tracks various performance metrics of the simulation.
    """
    def __init__(self):
        self.vehicle_lifetimes = {}
        self.name = "Network"
        self.metrics_for_stats: dict[str, float | int | list[float]] = {
            'stop_time': 0,
            'completed_lifetimes': [],
            'arrival_rate': 0.0,
            'throughput': 0.0,
            'utilization': 0.0,
            'average_time_service': 0.0,
        }
        self.T = 0
        self.arrivals = 0   # number of vehicles that arrived in the system
        self.completed = 0  # number of vehicles that completed their trip
        self.rq_time = 0    # time in which there is at least one request in the system

    def update(self):
        self.T += 1
        self.incoming_vehicles()
        self.outgoing_vehicles()

    def incoming_vehicles(self):
        there_is_request = False
        # Get a list of all vehicles currently in the simulation
        for vehicle_id in traci.vehicle.getIDList():
            there_is_request = True
            if vehicle_id not in self.vehicle_lifetimes:    # If the vehicle is seen for the first time, record its departure time
                self.arrivals += 1
                self.vehicle_lifetimes[vehicle_id] = traci.vehicle.getDeparture(vehicle_id)
            
            if traci.vehicle.getSpeed(vehicle_id) < 0.1:    # If the vehicle's speed is close to 0, increment stop_time
                self.metrics_for_stats['stop_time'] += 1
        if(there_is_request):
            self.rq_time += 1

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

class JointTracker(PerformanceTracker):
    def __init__(self, junction: str):
        super().__init__()
        self.junction = junction
        self.name = f"Junction_{junction}"

        self.outgoing_routes = [e for e in traci.junction.getOutgoingEdges(junction) if not e.startswith(":")]
        self.incoming_routes = [e for e in traci.junction.getIncomingEdges(junction) if not e.startswith(":")]

    def incoming_vehicles(self):
        there_is_request = False
        for vehicle_id in traci.vehicle.getIDList():

            current_edge = traci.vehicle.getRoadID(vehicle_id)
            if current_edge in self.incoming_routes: 
                there_is_request = True
                if vehicle_id not in self.vehicle_lifetimes:
                    self.arrivals += 1
                    self.vehicle_lifetimes[vehicle_id] = self.T
                
                if traci.vehicle.getSpeed(vehicle_id) < 0.1:
                    self.metrics_for_stats['stop_time'] += 1

        if there_is_request:
            self.rq_time += 1

    def outgoing_vehicles(self):
        for vehicle_id in traci.vehicle.getIDList():
            current_edge = traci.vehicle.getRoadID(vehicle_id)
            if current_edge in self.outgoing_routes:
                 # Calculate the lifetime and store it
                depart_time = self.vehicle_lifetimes.pop(vehicle_id, None)
                if depart_time is not None:
                    self.completed += 1
                    lifetime = self.T - depart_time
                    self.metrics_for_stats['completed_lifetimes'].append(lifetime)
       

if __name__ == "__main__":
    track = PerformanceTracker()
    # Cycle through all keys and values in self.metrics_for_stats
    for key, value in track.metrics_for_stats.items():
        print(key)
        