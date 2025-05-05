import traci
import traci._junction
import itertools
import traci.constants as tc

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

        self.subtracker = [JointTracker(DIRECTIONS[0]), FirstJoint()]
        # self.subtracker = [FirstJoint()]
        for sub in self.subtracker:
            sub.get_roads_from_junction()
            
            # Convert route lists to sets for faster lookups
            sub.incoming_routes = set(sub.incoming_routes)
            sub.outgoing_routes = set(sub.outgoing_routes)
            sub.incoming_junctions = list(itertools.chain.from_iterable(sub.incoming_junctions))
            sub.incoming_junctions = set(sub.incoming_junctions)
        
        self.name = "Network"
        self.subscribed_vehicles = set()  # Keep track of subscribed vehicles

    def update(self):
        self.T += 1
        
        # Get current vehicles in simulation
        current_vehicles = set(traci.vehicle.getIDList())
        
        # Subscribe to new vehicles
        for vehicle_id in current_vehicles:
            if vehicle_id not in self.subscribed_vehicles:
                traci.vehicle.subscribe(vehicle_id, [tc.VAR_ROAD_ID, tc.VAR_SPEED])
                self.subscribed_vehicles.add(vehicle_id)
        
        # Get all vehicle data at once
        vehicle_data = traci.vehicle.getAllSubscriptionResults()
        
        # Process each vehicle
        for vehicle_id, data in vehicle_data.items():
            current_edge = data[tc.VAR_ROAD_ID]
            vehicle_speed = data[tc.VAR_SPEED]
            
            for subtracker in self.subtracker:
                subtracker.T = self.T
                subtracker.process_vehicle(vehicle_id, current_edge, vehicle_speed)
        
        # Clean up subscriptions for vehicles that left the simulation
        departed_vehicles = self.subscribed_vehicles - current_vehicles
        for vehicle_id in departed_vehicles:
            self.subscribed_vehicles.remove(vehicle_id)
            # TraCI automatically unsubscribes departed vehicles, so no explicit unsubscribe needed
        
        # Update request time counters
        for subtracker in self.subtracker:
            if len(subtracker.vehicle_lifetimes) > 0:
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

        self.direction = direction
        self.name = f"Network_{direction}"
        self.request_monitor = False

    def get_roads_from_junction(self):
        for junction in NETWORK_JUNCTION:
            self.outgoing_routes.append([e for e in traci.junction.getOutgoingEdges(junction) if not e.startswith(":") and e.endswith(self.direction)])
            self.incoming_routes.append([e for e in traci.junction.getIncomingEdges(junction) if not e.startswith(":") and e.endswith(self.direction)])
            self.incoming_junctions.append([e for e in traci.junction.getIncomingEdges(junction) if e.startswith(":") and e.endswith(self.direction)])

        self.outgoing_routes = list(itertools.chain.from_iterable(self.outgoing_routes))
        self.incoming_routes = list(itertools.chain.from_iterable(self.incoming_routes))

    def process_vehicle(self, vehicle_id, current_edge, vehicle_speed):
        """Process vehicle data from subscription in a single pass"""
        # Handle incoming vehicles
        is_relevant_edge = (current_edge in self.incoming_junctions or 
                 (current_edge in self.incoming_routes and vehicle_speed < 0.1))
        
        if is_relevant_edge and vehicle_id not in self.vehicle_lifetimes:
            self.request_monitor = True
            self.arrivals += 1
            self.vehicle_lifetimes[vehicle_id] = traci.simulation.getTime()

        # Track stopped vehicles
        if vehicle_speed < 0.1:
            self.metrics_for_stats['stop_time'] += 1
            
        # Handle outgoing vehicles
        if current_edge in self.outgoing_routes:
            depart_time = self.vehicle_lifetimes.pop(vehicle_id, None)
            if depart_time is not None:
                self.completed += 1
                lifetime = traci.simulation.getTime() - depart_time
                self.metrics_for_stats['completed_lifetimes'].append(lifetime)

    # Legacy methods for backward compatibility
    def incoming_vehicles(self, vehicle_id):
        # This method is kept for backward compatibility but should not be used anymore
        pass
        
    def outgoing_vehicles(self, vehicle_id):
        # This method is kept for backward compatibility but should not be used anymore
        pass
       
    def simulation_end(self):
        # Adding safety checks to avoid division by zero
        self.metrics_for_stats['arrival_rate'] = self.arrivals / self.T if self.T > 0 else 0
        self.metrics_for_stats['throughput'] = self.completed / self.T if self.T > 0 else 0
        self.metrics_for_stats['utilization'] = self.rq_time / self.T if self.T > 0 else 0
        self.metrics_for_stats['average_time_service'] = self.rq_time / self.completed if self.completed > 0 else 0
        self.metrics_for_stats['completed'] = self.completed


class FirstJoint(JointTracker):
    def __init__(self):
        super().__init__("tang")
        self.name = f"first_servant"

    def get_roads_from_junction(self):
        self.outgoing_routes = ["E2"]
        self.incoming_routes = ["E0.66_tang"]